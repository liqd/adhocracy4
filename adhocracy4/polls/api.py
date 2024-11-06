import json
import re
import uuid

import requests
from django.apps import apps
from django.conf import settings
from django.db import transaction
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch
from django.utils.translation import gettext as _
from rest_framework import mixins
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.exceptions import ParseError
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from adhocracy4.api.permissions import ViewSetRulesPermission

from . import validators
from .models import Answer
from .models import Choice
from .models import OtherVote
from .models import Poll
from .models import Question
from .models import Vote
from .serializers import PollSerializer
from .signals import poll_voted


class PollViewSet(
    mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet
):
    """ViewSet used to edit a poll from the dashboard and to display and vote on the
    user side."""

    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    permission_classes = (ViewSetRulesPermission,)

    def get_permission_object(self):
        poll = self.get_object()
        return poll.module

    @property
    def rules_method_map(self):
        """This modifies the default rules to require the add_vote permission to POST
        instead of the default add_poll. This works because we only allow POST for
        votes and not for creating Polls."""
        return ViewSetRulesPermission.default_rules_method_map._replace(
            POST="a4polls.add_vote",
        )

    def _get_org_terms_model(self):
        """Make sure, only used with A4_USE_ORGANISATION_TERMS_OF_USE."""
        organisation_model = apps.get_model(settings.A4_ORGANISATIONS_MODEL)
        OrganisationTermsOfUse = apps.get_model(
            organisation_model._meta.app_label, "OrganisationTermsOfUse"
        )
        return OrganisationTermsOfUse

    def _user_has_agreed(self, user):
        if not user.is_authenticated:
            return False
        OrganisationTermsOfUse = self._get_org_terms_model()
        organisation = self.get_object().project.organisation
        user_has_agreed = OrganisationTermsOfUse.objects.filter(
            user=user, organisation=organisation, has_agreed=True
        ).exists()
        return user_has_agreed

    def add_terms_of_use_info(self, request, data):
        use_org_terms_of_use = False
        if (
            hasattr(settings, "A4_USE_ORGANISATION_TERMS_OF_USE")
            and settings.A4_USE_ORGANISATION_TERMS_OF_USE
        ):
            user_has_agreed = False
            use_org_terms_of_use = True
            organisation = self.get_object().project.organisation
            try:
                org_terms_url = reverse(
                    "organisation-terms-of-use",
                    kwargs={"organisation_slug": organisation.slug},
                )
            except NoReverseMatch:
                raise NotImplementedError("Add org terms of use view.")
            if hasattr(request, "user"):
                user = request.user
                if user.is_authenticated:
                    user_has_agreed = self._user_has_agreed(user)
            data["user_has_agreed"] = user_has_agreed
            data["org_terms_url"] = org_terms_url
        data["use_org_terms_of_use"] = use_org_terms_of_use
        return data

    def retrieve(self, request, *args, **kwargs):
        """Add organisation terms of use info to response.data."""
        response = super().retrieve(request, args, kwargs)
        if response.status_code == 400:
            return response
        response.data = self.add_terms_of_use_info(request, response.data)
        return response

    def __verify_captcha(self, answer, session):
        if hasattr(settings, "CAPTCHA_TEST_ACCEPTED_ANSWER"):
            return answer == settings.CAPTCHA_TEST_ACCEPTED_ANSWER

        if not hasattr(settings, "CAPTCHA_URL"):
            return False

        url = settings.CAPTCHA_URL
        data = {"session_id": session, "answer_id": answer, "action": "verify"}
        response = requests.post(url, data)
        return json.loads(response.text)["result"]

    def check_captcha(self):
        if not self.request.data.get("captcha", False):
            raise ValidationError(_("Your answer to the captcha was wrong."))

        combined_answer = self.request.data["captcha"].split(":")
        if len(combined_answer) != 2:
            raise ValidationError(
                _("Something about the answer to the captcha was wrong.")
            )

        answer, session = combined_answer

        if not re.match(r"[0-9a-zA-ZäöüÄÖÜß]+", answer) or not re.match(
            r"[0-9a-fA-F]+", session
        ):
            raise ValidationError(
                _("Something about the answer to the captcha was wrong.")
            )

        if not self.__verify_captcha(answer, session):
            raise ValidationError(_("Your answer to the captcha was wrong."))

    def check_terms_of_use(self):
        if getattr(
            settings, "A4_USE_ORGANISATION_TERMS_OF_USE", False
        ) and not self._user_has_agreed(self.request.user):
            if self.request.data.get("agreed_terms_of_use", False):
                if self.request.user.is_authenticated:
                    OrganisationTermsOfUse = self._get_org_terms_model()
                    OrganisationTermsOfUse.objects.update_or_create(
                        user=self.request.user,
                        organisation=self.get_object().project.organisation,
                        defaults={
                            "has_agreed": self.request.data["agreed_terms_of_use"]
                        },
                    )
            else:
                raise ValidationError(
                    {_("Please agree to the organisation's terms of use.")}
                )

    @action(detail=True, methods=["post"], permission_classes=[ViewSetRulesPermission])
    def vote(self, request, pk):
        if not self.request.user.is_authenticated:
            self.check_captcha()
        self.check_terms_of_use()

        creator = None
        content_id = None
        if self.request.user.is_authenticated:
            creator = self.request.user
        else:
            content_id = uuid.uuid4()
        for question_id in request.data["votes"]:
            question = self.get_question(question_id)
            validators.question_belongs_to_poll(question, int(pk))
            vote_data = self.request.data["votes"][question_id]
            self.save_vote(question, vote_data, creator, content_id)

        poll = self.get_object()
        poll_voted.send(
            sender=self.__class__, poll=poll, creator=creator, content_id=content_id
        )
        poll_serializer = self.get_serializer(poll)
        poll_data = self.add_terms_of_use_info(request, poll_serializer.data)
        if not self.request.user.is_authenticated:
            # set poll to read only after voting to prevent users from seeing the
            # voting screen again
            poll_data["questions"][0]["isReadOnly"] = True
        return Response(poll_data, status=status.HTTP_201_CREATED)

    def save_vote(self, question, vote_data, creator, content_id):
        choices, other_choice_answer, open_answer = self.get_data(vote_data)

        if not question.is_open:
            self.validate_choices(question, choices)

        with transaction.atomic():

            if question.is_open:
                self.clear_open_answer(question)
                if open_answer:
                    Answer.objects.create(
                        question=question,
                        answer=open_answer,
                        creator=creator,
                        content_id=content_id,
                    )
            else:
                self.clear_current_choices(question)
                for choice in choices:
                    vote = Vote.objects.create(
                        choice_id=choice.id, creator=creator, content_id=content_id
                    )
                    if choice.is_other_choice:
                        if other_choice_answer:
                            OtherVote.objects.create(
                                vote=vote, answer=other_choice_answer
                            )
                        else:
                            raise ValidationError(
                                {"choice": _("Please specify your answer.")}
                            )

    def get_data(self, vote_data):
        try:
            choices = [
                get_object_or_404(Choice, pk=choice_pk)
                for choice_pk in vote_data["choices"]
            ]
            other_choice_answer = vote_data["other_choice_answer"]
            open_answer = vote_data["open_answer"]
        except (ValueError, AttributeError):
            raise ValidationError()
        except KeyError as error:
            raise ParseError(detail=_("Key error for {}").format(str(error)))
        except Http404:
            raise NotFound(detail=_("Choice not found."))

        return choices, other_choice_answer, open_answer

    def get_question(self, id):
        return get_object_or_404(Question, pk=id)

    def clear_open_answer(self, question):
        if self.request.user.is_authenticated:
            Answer.objects.filter(
                question_id=question.id, creator=self.request.user
            ).delete()

    def clear_current_choices(self, question):
        if self.request.user.is_authenticated:
            Vote.objects.filter(
                choice__question_id=question.id, creator=self.request.user
            ).delete()

    def validate_choices(self, question, choices):
        if len(choices) > len(set(choices)):
            raise ValidationError(detail=_("Duplicate choices detected."))

        elif len(choices) > 1 and not question.multiple_choice:
            raise ValidationError(detail=_("Multiple choice disabled for " "question."))

        for choice in choices:
            validators.choice_belongs_to_question(choice, question.pk)

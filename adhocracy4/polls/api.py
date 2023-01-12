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


class PollViewSet(
    mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet
):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    permission_classes = (ViewSetRulesPermission,)

    def get_permission_object(self):
        poll = self.get_object()
        return poll.module

    @property
    def rules_method_map(self):
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
            user_has_agreed = None
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

    @action(detail=True, methods=["post"], permission_classes=[ViewSetRulesPermission])
    def vote(self, request, pk):
        if (
            hasattr(settings, "A4_USE_ORGANISATION_TERMS_OF_USE")
            and settings.A4_USE_ORGANISATION_TERMS_OF_USE
            and not self._user_has_agreed(self.request.user)
        ):
            if (
                "agreed_terms_of_use" in self.request.data
                and self.request.data["agreed_terms_of_use"]
            ):
                OrganisationTermsOfUse = self._get_org_terms_model()
                OrganisationTermsOfUse.objects.update_or_create(
                    user=self.request.user,
                    organisation=self.get_object().project.organisation,
                    defaults={"has_agreed": self.request.data["agreed_terms_of_use"]},
                )
            else:
                raise ValidationError(
                    {_("Please agree to the organisation's terms of use.")}
                )

        for question_id in request.data["votes"]:
            question = self.get_question(question_id)
            validators.question_belongs_to_poll(question, int(pk))
            vote_data = self.request.data["votes"][question_id]
            self.save_vote(question, vote_data)

        poll = self.get_object()
        poll_serializer = self.get_serializer(poll)
        poll_data = self.add_terms_of_use_info(request, poll_serializer.data)
        return Response(poll_data, status=status.HTTP_201_CREATED)

    def save_vote(self, question, vote_data):
        choices, other_choice_answer, open_answer = self.get_data(vote_data)

        if not question.is_open:
            self.validate_choices(question, choices)

        with transaction.atomic():
            if question.is_open:
                self.clear_open_answer(question)
                if open_answer:
                    Answer.objects.create(
                        question=question, answer=open_answer, creator=self.request.user
                    )
            else:
                self.clear_current_choices(question)
                for choice in choices:
                    vote = Vote.objects.create(
                        choice_id=choice.id, creator=self.request.user
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
        Answer.objects.filter(
            question_id=question.id, creator=self.request.user
        ).delete()

    def clear_current_choices(self, question):
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

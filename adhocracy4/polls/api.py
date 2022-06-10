from django.conf import settings
from django.db import transaction
from django.http import Http404
from django.shortcuts import get_object_or_404
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


class PollViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    permission_classes = (ViewSetRulesPermission,)

    def get_permission_object(self):
        poll = self.get_object()
        return poll.module

    @property
    def rules_method_map(self):
        return ViewSetRulesPermission.default_rules_method_map._replace(
            POST='a4polls.add_vote',
        )

    def retrieve(self, request, *args, **kwargs):
        """Add organisation terms of use info to response.data."""
        response = super().retrieve(request, args, kwargs)
        if response.status_code == 400:
            return response

        use_org_terms_of_use = False
        if hasattr(settings, 'A4_USE_ORGANISATION_TERMS_OF_USE') \
           and settings.A4_USE_ORGANISATION_TERMS_OF_USE:
            user_has_agreed = None
            use_org_terms_of_use = True
            if hasattr(request, 'user'):
                user = request.user
                if user.is_authenticated:
                    organisation = self.get_object().project.organisation
                    user_has_agreed = \
                        user.has_agreed_on_org_terms(organisation)
            response.data['user_has_agreed'] = user_has_agreed
        response.data['use_org_terms_of_use'] = use_org_terms_of_use
        return response

    @action(detail=True, methods=['post'],
            permission_classes=[ViewSetRulesPermission])
    def vote(self, request, pk):
        for question_id in request.data['votes']:
            question = self.get_question(question_id)
            validators.question_belongs_to_poll(question, int(pk))
            vote_data = self.request.data['votes'][question_id]
            self.save_vote(question, vote_data)
        poll = self.get_object()
        poll_serializer = self.get_serializer(poll)
        return Response(poll_serializer.data,
                        status=status.HTTP_201_CREATED)

    def save_vote(self, question, vote_data):
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
                        creator=self.request.user
                    )
            else:
                self.clear_current_choices(question)
                for choice in choices:
                    vote = Vote.objects.create(
                        choice_id=choice.id,
                        creator=self.request.user
                    )
                    if choice.is_other_choice:
                        if other_choice_answer:
                            OtherVote.objects.create(
                                vote=vote,
                                answer=other_choice_answer
                            )
                        else:
                            raise ValidationError({
                                'choice': _('Please specify your answer.')
                            })

    def get_data(self, vote_data):
        try:
            choices = [get_object_or_404(Choice, pk=choice_pk)
                       for choice_pk
                       in vote_data['choices']]
            other_choice_answer = vote_data['other_choice_answer']
            open_answer = vote_data['open_answer']
        except (ValueError, AttributeError):
            raise ValidationError()
        except KeyError as error:
            raise ParseError(detail=_('Key error for {}').format(str(error)))
        except Http404:
            raise NotFound(detail=_('Choice not found.'))

        return choices, other_choice_answer, open_answer

    def get_question(self, id):
        return get_object_or_404(
            Question,
            pk=id
        )

    def clear_open_answer(self, question):
        Answer.objects\
            .filter(question_id=question.id,
                    creator=self.request.user)\
            .delete()

    def clear_current_choices(self, question):
        Vote.objects\
            .filter(choice__question_id=question.id,
                    creator=self.request.user)\
            .delete()

    def validate_choices(self, question, choices):
        if len(choices) > len(set(choices)):
            raise ValidationError(detail=_('Duplicate choices detected.'))

        elif len(choices) > 1 and not question.multiple_choice:
            raise ValidationError(detail=_('Multiple choice disabled for '
                                           'question.'))

        for choice in choices:
            validators.choice_belongs_to_question(choice, question.pk)

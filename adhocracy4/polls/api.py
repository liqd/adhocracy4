from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import mixins
from rest_framework import status
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from adhocracy4.api.permissions import ViewSetRulesPermission

from .models import Answer
from .models import Choice
from .models import OtherVote
from .models import Poll
from .models import Question
from .models import Vote
from .serializers import PollSerializer
from .serializers import QuestionSerializer
from .validators import choice_belongs_to_question


class PollViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    permission_classes = (ViewSetRulesPermission,)

    def get_permission_object(self):
        poll = self.get_object()
        return poll.module


class VoteViewSet(viewsets.ViewSet):

    permission_classes = (ViewSetRulesPermission,)

    def create(self, request, *args, **kwargs):
        choices, other_choice_answer, open_answer = self.get_data(request)

        self.validate_choices(choices)

        with transaction.atomic():
            if self.question.is_open:
                self.clear_open_answer()
                Answer.objects.create(
                    question=self.question,
                    answer=open_answer,
                    creator=self.request.user
                )
            else:
                self.clear_current_choices()
                for choice in choices:
                    vote = Vote.objects.create(
                        choice_id=choice.id,
                        creator=self.request.user
                    )
                    if choice.is_other_choice:
                        OtherVote.objects.create(
                            vote=vote,
                            answer=other_choice_answer
                        )

        question_serializer = self.get_question_serializer()
        return Response({'question': question_serializer.data},
                        status=status.HTTP_201_CREATED)

    def get_data(self, request):
        try:
            choices = [get_object_or_404(Choice, pk=choice_pk)
                       for choice_pk
                       in request.data['choices']]
        except (ValueError, AttributeError):
            raise ValidationError()

        other_choice_answer = request.data['other_choice_answer']

        open_answer = request.data['open_answer']

        return choices, other_choice_answer, open_answer

    def validate_choices(self, choices):
        question = self.question

        if len(choices) > len(set(choices)):
            raise ValidationError('duplicate choices detected')

        if len(choices) == 0:
            raise ValidationError('empty choices detected')
        elif len(choices) > 1 and not question.multiple_choice:
            raise ValidationError('multiple choice disabled for question')

        for choice in choices:
            choice_belongs_to_question(choice, question.pk)

    def clear_current_choices(self):
        Vote.objects\
            .filter(choice__question_id=self.question.id,
                    creator=self.request.user)\
            .delete()

    def clear_open_answer(self):
        Answer.objects\
            .filter(question_id=self.question.id,
                    creator=self.request.user)\
            .delete()

    @property
    def question(self):
        return get_object_or_404(
            Question,
            pk=self.kwargs['question_pk']
        )

    def get_question_serializer(self):
        question = Question.objects\
            .annotate_vote_count()\
            .get(pk=self.kwargs['question_pk'])

        return QuestionSerializer(
            question,
            context={
                'request': self.request
            }
        )

    def get_queryset(self):
        return Vote.objects.filter(
            choice__question_id=self.kwargs['question_pk'])

    def get_permission_object(self):
        return self.question.poll.module

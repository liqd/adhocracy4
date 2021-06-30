from rest_framework import serializers

from adhocracy4.dashboard import components
from adhocracy4.dashboard import signals as a4dashboard_signals
from adhocracy4.rules.discovery import NormalUser

from . import models


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Answer
        fields = ('id', 'answer')


class OtherChoiceAnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.OtherVote
        fields = ('vote_id', 'answer')


class ChoiceSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    count = serializers.SerializerMethodField()

    class Meta:
        model = models.Choice
        fields = ('id', 'label', 'count', 'is_other_choice')

    def get_count(self, choice):
        if hasattr(choice, 'vote_count'):
            return getattr(choice, 'vote_count', -1)
        else:
            return choice.votes.all().count()


class QuestionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    isReadOnly = serializers.SerializerMethodField('get_is_read_only')
    authenticated = serializers.SerializerMethodField()
    choices = ChoiceSerializer(many=True)
    userChoices = serializers.SerializerMethodField('get_user_choices')
    answers = AnswerSerializer(many=True)
    userAnswer = serializers.SerializerMethodField('get_user_answer')
    other_choice_answers = serializers.SerializerMethodField(
        'get_other_choice_answers')
    other_choice_user_answer = serializers.SerializerMethodField(
        'get_other_choice_user_answer')
    totalVoteCount = serializers.SerializerMethodField('get_total_vote_count')
    totalVoteCountMulti = serializers.SerializerMethodField(
        'get_total_vote_count_multi')
    totalAnswerCount = serializers.SerializerMethodField(
        'get_total_answer_count')

    class Meta:
        model = models.Question
        fields = ('id', 'label', 'help_text', 'multiple_choice', 'is_open',
                  'isReadOnly', 'authenticated', 'choices', 'userChoices',
                  'answers', 'userAnswer', 'other_choice_answers',
                  'other_choice_user_answer', 'totalVoteCount',
                  'totalVoteCountMulti', 'totalAnswerCount')

    def get_authenticated(self, _):
        if 'request' in self.context:
            user = self.context['request'].user
            return bool(user.is_authenticated)
        return False

    def get_is_read_only(self, question):
        if 'request' in self.context:
            user = self.context['request'].user
            has_poll_permission = user.has_perm(
                'a4polls.add_vote',
                question.poll.module
            )
            would_have_poll_permission = NormalUser().would_have_perm(
                'a4polls.add_vote',
                question.poll.module
            )
            return not has_poll_permission and not would_have_poll_permission

        return True

    def get_user_choices(self, question):
        if 'request' in self.context:
            user = self.context['request'].user
            return question.user_choices_list(user)
        return []

    def get_user_answer(self, question):
        if 'request' in self.context:
            user = self.context['request'].user
            return question.user_answer(user)
        return ''

    def get_other_choice_answers(self, question):
        other_choice_answers = question.other_choice_answers()
        serializer = OtherChoiceAnswerSerializer(
            instance=other_choice_answers,
            many=True)
        return serializer.data

    def get_other_choice_user_answer(self, question):
        if 'request' in self.context:
            user = self.context['request'].user
            return question.other_choice_user_answer(user)
        return ''

    def get_total_vote_count(self, question):
        return getattr(question, 'vote_count', -1)

    def get_total_vote_count_multi(self, question):
        return getattr(question, 'vote_count_multi', -1)

    def get_total_answer_count(self, question):
        return getattr(question, 'answer_count', -1)


class PollSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, source='annotated_questions')

    class Meta:
        model = models.Poll
        fields = ('id', 'questions')

    def update(self, instance, data):
        # Delete removed questions from the database
        instance.questions.exclude(
            id__in=[question['id']
                    for question in data['annotated_questions']
                    if 'id' in question
                    ]).delete()

        # Update (or create) the questions
        for weight, question in enumerate(data['annotated_questions']):
            question_id = question.get('id')
            question_instance, _ = models.Question.objects.update_or_create(
                id=question_id,
                defaults={
                    'poll': instance,
                    'label': question['label'],
                    'help_text': question['help_text'],
                    'multiple_choice': question['multiple_choice'],
                    'is_open': question['is_open'],
                    'weight': weight
                })
            if not question['is_open']:
                self._update_choices(question, question_instance)

        # Send the component updated signal
        # (the serializer is only used from within the dashboard)
        self._send_component_updated_signal(instance)

        return instance

    def _update_choices(self, question, question_instance):
        # Delete removed choices from the database
        choice_ids = [choice['id']
                      for choice in question['choices']
                      if 'id' in choice]
        question_instance.choices.exclude(id__in=choice_ids).delete()

        # Update (or create) this questions choices
        for choice in question['choices']:
            choice_id = choice.get('id')
            choice_instance, _ = models.Choice.objects.update_or_create(
                id=choice_id,
                defaults={
                    'question': question_instance,
                    'label': choice['label'],
                    'is_other_choice': choice['is_other_choice']
                }
            )

    def _send_component_updated_signal(self, question_instance):
        component = components.modules['polls']
        a4dashboard_signals.module_component_updated.send(
            sender=component.__class__,
            module=question_instance.module,
            component=component.__class__,
            user=self.context['request'].user
        )

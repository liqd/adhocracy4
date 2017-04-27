from rest_framework import serializers

from . import models


class ChoiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Choice
        fields = ('id', 'label')


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True)

    class Meta:
        model = models.Question
        fields = ('id', 'label', 'weight', 'choices')


class PollSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = models.Poll
        fields = ('id', 'questions')

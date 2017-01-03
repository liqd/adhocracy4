from django.views.generic import list

from . import models


class QuestionList(list.ListView):
    model = models.Question

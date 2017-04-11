from adhocracy4.modules import forms as module_forms
from . import models


class QuestionForm(module_forms.ItemForm):

    class Meta:
        model = models.Question
        fields = ['text']

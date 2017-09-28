from django import forms

from adhocracy4.categories.forms import CategorizableFieldMixin

from . import models


class TopicForm(CategorizableFieldMixin, forms.ModelForm):

    class Meta:
        model = models.Topic
        fields = ['name', 'description', 'category']

from adhocracy4.categories import forms as category_forms

from . import models


class TopicForm(category_forms.CategorizableForm):

    class Meta:
        model = models.Topic
        fields = ['name', 'description', 'category']

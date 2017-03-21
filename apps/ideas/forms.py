from adhocracy4.categories import forms as category_forms

from . import models


class IdeaForm(category_forms.CategorizableForm):

    class Meta:
        model = models.Idea
        fields = ['name', 'description', 'category']

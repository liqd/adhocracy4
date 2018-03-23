from django import forms

from adhocracy4.categories.forms import CategorizableFieldMixin
from meinberlin.apps.contrib.mixins import ImageRightOfUseMixin

from . import models


class IdeaForm(CategorizableFieldMixin, ImageRightOfUseMixin):

    class Meta:
        model = models.Idea
        fields = ['name', 'description', 'image', 'category']


class IdeaModerateForm(forms.ModelForm):
    class Meta:
        model = models.Idea
        fields = ['moderator_feedback']

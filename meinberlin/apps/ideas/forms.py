from django import forms

from adhocracy4.categories.forms import CategorizableFieldMixin
from adhocracy4.labels.mixins import LabelsAddableFieldMixin
from meinberlin.apps.contrib.mixins import ImageRightOfUseMixin

from . import models


class IdeaForm(CategorizableFieldMixin,
               LabelsAddableFieldMixin,
               ImageRightOfUseMixin):

    class Meta:
        model = models.Idea
        fields = ['name', 'description', 'image', 'category', 'labels']


class IdeaModerateForm(forms.ModelForm):
    class Meta:
        model = models.Idea
        fields = ['moderator_feedback']

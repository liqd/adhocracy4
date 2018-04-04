from django import forms

from meinberlin.apps.contrib.mixins import ImageRightOfUseMixin
from meinberlin.apps.mapideas.forms import MapIdeaForm

from . import models


class ProposalForm(MapIdeaForm, ImageRightOfUseMixin):

    class Meta:
        model = models.Proposal
        fields = ['name', 'description', 'image',
                  'category', 'budget', 'point',
                  'point_label']


class ProposalModerateForm(forms.ModelForm):
    class Meta:
        model = models.Proposal
        fields = ['moderator_feedback', 'is_archived']

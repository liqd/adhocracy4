from django import forms

from meinberlin.apps.mapideas.forms import MapIdeaForm

from . import models


class ProposalForm(MapIdeaForm):

    class Meta:
        model = models.Proposal
        fields = ['name', 'description', 'category', 'labels',
                  'image', 'budget', 'creator_contribution',
                  'point', 'point_label']


class ProposalModerateForm(forms.ModelForm):
    class Meta:
        model = models.Proposal
        fields = ['moderator_feedback']

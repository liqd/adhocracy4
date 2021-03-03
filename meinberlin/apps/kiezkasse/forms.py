from django import forms

from meinberlin.apps.contrib.widgets import Select2Widget
from meinberlin.apps.mapideas.forms import MapIdeaForm

from . import models


class ProposalForm(MapIdeaForm):

    class Meta:
        model = models.Proposal
        fields = ['name', 'description', 'category', 'labels',
                  'image', 'budget', 'creator_contribution',
                  'point', 'point_label']
        widgets = {
            'category': Select2Widget(attrs={'class': 'select2__no-search'})
        }


class ProposalModerateForm(forms.ModelForm):
    class Meta:
        model = models.Proposal
        fields = ['moderator_feedback']

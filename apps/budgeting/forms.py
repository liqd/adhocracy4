from django import forms

from adhocracy4.categories import forms as category_forms

from . import models


class ProposalForm(category_forms.CategorizableForm):

    class Meta:
        model = models.Proposal
        fields = ['name', 'description', 'category', 'budget']


class ProposalModerateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        kwargs.pop('module')
        super(ProposalModerateForm, self).__init__(*args, **kwargs)

    class Meta:
        model = models.Proposal
        fields = ['moderator_feedback']

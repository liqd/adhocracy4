from adhocracy4.categories import forms as category_forms

from . import models


class ProposalForm(category_forms.CategorizableForm):

    class Meta:
        model = models.Proposal
        fields = ['name', 'description', 'category', 'budget']

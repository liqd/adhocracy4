from django import forms
from multiform import MultiModelForm

from adhocracy4.categories import forms as category_forms

from . import models


class ProposalForm(category_forms.CategorizableForm):

    class Meta:
        model = models.Proposal
        fields = ['name', 'description', 'category', 'budget']


class ModeratorFeedbackForm(forms.ModelForm):

    class Meta:
        model = models.Proposal
        fields = ['moderator_feedback']


class ModeratorStatementForm(forms.ModelForm):

    class Meta:
        model = models.ModeratorStatement
        fields = ['statement']


class ProposalModerateForm(MultiModelForm):
    base_forms = [
        ('feedback', ModeratorFeedbackForm),
        ('statement', ModeratorStatementForm),
    ]

    def __init__(self, creator, *args, **kwargs):
        self.creator = creator
        self.proposal = kwargs['instance']
        super(ProposalModerateForm, self).__init__(*args, **kwargs)

    def dispatch_init_instance(self, name, instance):
        if name == 'feedback':
            return instance

        if name == 'statement':
            try:
                statement = instance.moderator_statement
                return statement
            except models.Proposal.moderator_statement\
                    .RelatedObjectDoesNotExist:
                return None

        return super(ProposalModerateForm, self)\
            .dispatch_init_instance(name, instance)

    def save(self, commit=True):
        statement_form = self.forms['statement']
        if statement_form.instance.pk is None:
            statement_form.instance.creator = self.creator
            statement_form.instance.proposal = self.proposal

        return super(ProposalModerateForm, self).save(commit)

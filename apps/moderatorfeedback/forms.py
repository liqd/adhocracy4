from django import forms
from django.core.exceptions import ObjectDoesNotExist
from multiform import MultiModelForm

from . import models


class ModeratorStatementForm(forms.ModelForm):
    class Meta:
        model = models.ModeratorStatement
        fields = ['statement']


def moderator_feedback_form_factory(model):
    meta_cls = type('Meta',
                    (AbstractModeratorFeedbackForm.Meta,),
                    {'model': model})
    form_cls = type('%sModeratorFeedbackForm' % model.__name__,
                    (AbstractModeratorFeedbackForm,),
                    {'Meta': meta_cls})
    return form_cls


class AbstractModeratorFeedbackForm(forms.ModelForm):
    class Meta:
        fields = ['moderator_feedback']


def item_moderate_form_factory(model):
    base_forms = [
        ('feedback', moderator_feedback_form_factory(model)),
        ('statement', ModeratorStatementForm),
    ]

    form_cls = type('%sProposalModerateForm' % model.__name__,
                    (AbstractProposalModerateForm,),
                    {'base_forms': base_forms})
    return form_cls


class AbstractProposalModerateForm(MultiModelForm):
    def __init__(self, item, creator, *args, **kwargs):
        self.item = item
        self.creator = creator
        super(AbstractProposalModerateForm, self).__init__(*args, **kwargs)

    def dispatch_init_instance(self, name, instance):
        if name == 'feedback':
            return self.item

        if name == 'statement':
            try:
                statement = self.item.moderator_statement
                return statement
            except ObjectDoesNotExist:
                return None

        return super(AbstractProposalModerateForm, self)\
            .dispatch_init_instance(name, instance)

    def save(self, commit=True):
        statement = self.forms['statement'].instance

        # If a new statement is created, it has to saved and
        # stored to the item explicitly
        if statement.pk is None:
            statement.creator = self.creator
            statement.save()
            self.item.moderator_statement = statement
            self.item.save()

        return super(AbstractProposalModerateForm, self).save(commit)

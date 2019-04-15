from django import forms
from django.apps import apps
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from adhocracy4.projects.models import Project

from . import models

Organisation = apps.get_model(settings.A4_ORGANISATIONS_MODEL)


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = models.Newsletter
        fields = ['sender_name', 'sender', 'receivers', 'project',
                  'organisation', 'subject', 'body']

    def __init__(self, user=None, organisation=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choices = [(value, string)
                   for value, string in models.RECEIVER_CHOICES
                   if value != models.PLATFORM or (user and user.is_superuser)]
        self.fields['receivers'] = forms.ChoiceField(
            label=_('Receivers'),
            choices=choices,
            widget=forms.RadioSelect(),
        )

        project_qs = Project.objects
        if organisation:
            project_qs = Project.objects.filter(organisation=organisation.id)

        self.fields['project'] = forms.ModelChoiceField(
            label=_('Project'),
            queryset=project_qs,
            required=False, empty_label=None)

        self.fields['organisation'] = forms.ModelChoiceField(
            label=_('Organisation'),
            queryset=Organisation.objects,
            required=False, empty_label=None)

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('receivers') == str(models.PROJECT) and \
                not cleaned_data.get('project'):
            self.add_error('project', _('Select a Project'))


class RestrictedNewsletterForm(forms.ModelForm):

    class Meta:
        model = models.Newsletter
        fields = ['sender_name', 'sender', 'project', 'receivers',
                  'organisation', 'subject', 'body']

    def __init__(self, user=None, organisation=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['receivers'].widget = forms.HiddenInput()

        project_qs = Project.objects
        if organisation:
            project_qs = Project.objects.filter(organisation=organisation.id)
            if user and not user.is_superuser:
                user_groups = user.groups.all()
                org_groups = organisation.groups.all()
                shared_groups = user_groups & org_groups
                group = shared_groups.distinct().first()
                project_qs = project_qs.filter(group=group)

        self.fields['project'] = forms.ModelChoiceField(
            label=_('Project'),
            queryset=project_qs,
            required=False, empty_label=None)
        self.fields['project'].label = _('Receivers are all users '
                                         'which follow the following project:')

        self.fields['organisation'] = forms.ModelChoiceField(
            label=_('Organisation'),
            queryset=Organisation.objects,
            required=False, empty_label=None)

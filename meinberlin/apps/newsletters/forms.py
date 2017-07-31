from django import forms
from django.apps import apps
from django.conf import settings

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
        self.fields['receivers'] = \
            forms.ChoiceField(choices=choices, widget=forms.RadioSelect())

        project_qs = Project.objects
        if organisation:
            project_qs = Project.objects.filter(organisation=organisation.id)

        self.fields['project'] = forms.ModelChoiceField(
            queryset=project_qs,
            required=False, empty_label=None)

        self.fields['organisation'] = forms.ModelChoiceField(
            queryset=Organisation.objects,
            required=False, empty_label=None)

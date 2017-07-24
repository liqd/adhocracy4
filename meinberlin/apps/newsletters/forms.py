from django import forms

from . import models
from .models import RECEIVER_CHOICES


class NewsletterForm(forms.ModelForm):

    class Meta:
        model = models.Newsletter
        fields = ['sender_name', 'sender', 'receivers', 'project',
                  'organisation', 'subject', 'body']

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choices = []
        for value, string in RECEIVER_CHOICES:
            if not user.is_superuser:
                if value != 0:
                    choices.append((value, string))
            else:
                choices.append((value, string))
        self.fields['receivers'] = \
            forms.ChoiceField(choices=choices, widget=forms.RadioSelect())

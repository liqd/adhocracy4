from django import forms

from . import models


class NewsletterForm(forms.ModelForm):

    class Meta:
        model = models.Newsletter
        fields = ['sender', 'receivers', 'project', 'organisation',
                  'subject', 'body']

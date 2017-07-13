from django import forms

from . import models


class NewsletterForm(forms.ModelForm):

    class Meta:
        model = models.Newsletter
        fields = ['sender_name', 'sender', 'receivers', 'project',
                  'organisation', 'subject', 'body']
        widgets = {
            'receivers': forms.RadioSelect()
        }

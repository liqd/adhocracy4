from django import forms

from .models import PlatformEmail


class PlatformEmailForm(forms.ModelForm):
    class Meta:
        model = PlatformEmail
        fields = ["sender_name", "sender", "subject", "body"]

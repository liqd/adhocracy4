from django import forms
from django.utils.translation import gettext_lazy as _

from .models import PlatformEmail


class PlatformEmailForm(forms.ModelForm):
    class Meta:
        model = PlatformEmail
        fields = ["sender_name", "sender", "subject", "body"]
        help_texts = {
            "body": _(
                "If you add an image, please provide an alternate text. "
                "It serves as a textual description of the image content "
                "and is read out by screen readers. Describe the image "
                "in approx. 80 characters. Example: A busy square with "
                "people in summer."
            ),
        }

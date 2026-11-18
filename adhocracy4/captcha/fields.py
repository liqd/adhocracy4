from django import forms
from django.utils.translation import gettext_lazy as _

from .verification import verify_cap_token
from .widgets import CapCaptchaWidget


class CapCaptchaField(forms.CharField):
    widget = CapCaptchaWidget

    def validate(self, value):
        super().validate(value)
        if not verify_cap_token(value):
            raise forms.ValidationError(_("Your answer to the captcha was wrong."))

from django import forms

from .widgets import CaptcheckCaptchaWidget


class CaptcheckCaptchaField(forms.CharField):
    widget = CaptcheckCaptchaWidget

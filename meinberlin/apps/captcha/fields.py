import json
import re

import requests
from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from .widgets import CaptcheckCaptchaWidget


class CaptcheckCaptchaField(forms.CharField):
    widget = CaptcheckCaptchaWidget

    def __verify_captcha(self, answer, session):
        if hasattr(settings, 'CAPTCHA_TEST_ACCEPTED_ANSWER'):
            return (answer == settings.CAPTCHA_TEST_ACCEPTED_ANSWER)

        if not hasattr(settings, 'CAPTCHA_URL'):
            return False

        url = settings.CAPTCHA_URL
        data = {
            'session_id': session,
            'answer_id': answer,
            'action': 'verify'
        }
        response = requests.post(url, data)
        return json.loads(response.text)['result']

    def validate(self, value):
        super().validate(value)

        combined_answer = value.split(':')
        if len(combined_answer) != 2:
            raise forms.ValidationError(
                _("Something about the answer to the captcha was wrong.")
            )

        if (
            not re.match(r"[0-9a-zA-ZäöüÄÖÜß]+", combined_answer[0]) or
            not re.match(r"[0-9a-fA-F]+", combined_answer[1])
        ):
            raise forms.ValidationError(
                _("Something about the answer to the captcha was wrong.")
            )

        if not self.__verify_captcha(combined_answer[0], combined_answer[1]):
            raise forms.ValidationError(
                _("Your answer to the captcha was wrong.")
            )

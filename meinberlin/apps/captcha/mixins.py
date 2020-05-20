import json

import requests
from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


class CaptcheckCaptchaFormMixin:

    def verify_captcha(self, answer, session):
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

    def clean_captcha(self):
        capt_answer = self.data.get('captcheck_selected_answer')
        capt_session = self.data.get('captcheck_session_code')
        if capt_answer:
            captcha_verified = self.verify_captcha(
                capt_answer, capt_session)
            if not captcha_verified:
                raise forms.ValidationError(
                    _("Your answer to the captcha was wrong."))
        else:
            raise forms.ValidationError(_("Please answer the captcha"))

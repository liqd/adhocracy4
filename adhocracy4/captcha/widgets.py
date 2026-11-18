from django import forms
from django.conf import settings
from django.utils.translation import get_language


class CapCaptchaWidget(forms.HiddenInput):
    template_name = "a4captcha/cap_captcha_widget.html"

    @property
    def media(self):
        js = []
        widget_url = getattr(settings, "A4_CAP_CAPTCHA_WIDGET_URL", "")
        if widget_url:
            js = ["a4captcha/cap_captcha.js", widget_url]
        return forms.Media(js=js)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context.update(
            {
                "endpoint": getattr(settings, "A4_CAP_CAPTCHA_ENDPOINT", ""),
                "wasm_url": getattr(settings, "A4_CAP_CAPTCHA_WASM_URL", ""),
                "hashwx_url": getattr(settings, "A4_CAP_CAPTCHA_HASHWX_URL", ""),
                "language_code": (get_language() or "en").split("-")[0],
            }
        )
        return context

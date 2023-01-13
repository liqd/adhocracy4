from django.conf import settings
from django.forms import widgets
from django.template import loader


class CaptcheckCaptchaWidget(widgets.HiddenInput):
    class Media:
        js = ("captcheck.js",)

    def render(self, name, value, attrs, renderer=None):

        context = {
            "name": name,
            "id": attrs.get("id"),
            "captcha_api_url": settings.CAPTCHA_URL,
        }

        return loader.render_to_string(
            "meinberlin_captcha/captcheck_captcha_widget.html", context
        )

import json

from django import template
from django.conf import settings
from django.utils.html import format_html
from django.utils.translation import get_language

from adhocracy4.polls.models import Poll

register = template.Library()


@register.simple_tag
def react_polls(poll: Poll):
    attributes = {
        "pollId": poll.pk,
        "captchaUrl": getattr(settings, "CAPTCHA_URL", ""),
        "captchaType": getattr(settings, "A4_CAPTCHA_TYPE", "captcheck"),
        "capCaptchaEndpoint": getattr(settings, "A4_CAP_CAPTCHA_ENDPOINT", ""),
        "capCaptchaWidgetUrl": getattr(settings, "A4_CAP_CAPTCHA_WIDGET_URL", ""),
        "capCaptchaWasmUrl": getattr(settings, "A4_CAP_CAPTCHA_WASM_URL", ""),
        "capCaptchaHashwxUrl": getattr(settings, "A4_CAP_CAPTCHA_HASHWX_URL", ""),
        "captchaLanguage": (get_language() or "en").split("-")[0],
        "questionImagesEnabled": getattr(settings, "A4_POLL_QUESTION_IMAGES", True),
    }

    extra = getattr(settings, "A4_POLL_TEMPLATE_TAG_EXTRA_ATTRIBUTES", {})
    if isinstance(extra, str):
        from django.utils.module_loading import import_string

        extra = import_string(extra)
    if callable(extra):
        extra = extra(poll)
    attributes.update(extra)

    return format_html(
        '<div data-a4-widget="polls" data-attributes="{attributes}"></div>',
        attributes=json.dumps(attributes),
    )


@register.simple_tag
def react_poll_form(poll, reload_on_success=False):
    attributes = {
        "pollId": poll.pk,
        "reloadOnSuccess": reload_on_success,
        "enableUnregisteredUsers": getattr(
            settings, "A4_POLL_ENABLE_UNREGISTERED_USERS", False
        ),
        "questionImagesEnabled": getattr(settings, "A4_POLL_QUESTION_IMAGES", True),
    }
    reload_on_success = json.dumps(reload_on_success)

    return format_html(
        '<div data-a4-widget="poll-management" data-attributes="{attributes}"></div>',
        attributes=json.dumps(attributes),
    )

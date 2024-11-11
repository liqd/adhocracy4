import json

from django import template
from django.conf import settings
from django.utils.html import format_html

from adhocracy4.polls.models import Poll

register = template.Library()


@register.simple_tag
def react_polls(poll: Poll):
    attributes = {"pollId": poll.pk, "captchaUrl": getattr(settings, "CAPTCHA_URL", "")}

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
    }
    reload_on_success = json.dumps(reload_on_success)

    return format_html(
        '<div data-a4-widget="poll-management" data-attributes="{attributes}"></div>',
        attributes=json.dumps(attributes),
    )

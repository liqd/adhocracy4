import json

from django import template
from django.conf import settings
from django.utils.html import format_html

from adhocracy4.open_poll.models import OpenPoll

register = template.Library()


@register.simple_tag
def react_open_poll(poll: OpenPoll):
    attributes = {
        "pollId": poll.pk,
        "captchaUrl": getattr(settings, "CAPTCHA_URL", "")
    }

    return format_html(
        '<div data-a4-widget="open-poll" data-attributes="{attributes}"></div>',
        attributes=json.dumps(attributes),
    )


@register.simple_tag
def react_open_poll_form(poll: OpenPoll, reload_on_success: bool = False):
    reload_on_success = json.dumps(reload_on_success)

    return format_html(
        (
            '<div data-a4-widget="open-poll-management" data-poll-id="{pollId}" '
            ' data-reloadOnSuccess="{reload_on_success}">'
            "</div>"
        ),
        pollId=poll.pk,
        reload_on_success=reload_on_success,
    )

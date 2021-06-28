import json

from django import template
from django.utils.html import format_html

register = template.Library()


@register.simple_tag
def react_polls(poll):
    return format_html(
        '<div data-a4-widget="polls" data-poll-id="{pollId}"></div>',
        pollId=poll.pk,
    )


@register.simple_tag
def react_poll_form(poll, reload_on_success=False):
    reload_on_success = json.dumps(reload_on_success)

    return format_html(
        (
            '<div data-a4-widget="poll-management" data-poll-id="{pollId}" '
            ' data-reloadOnSuccess="{reload_on_success}">'
            '</div>'
        ),
        pollId=poll.pk,
        reload_on_success=reload_on_success,
    )

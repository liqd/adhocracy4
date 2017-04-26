import json

from django import template
from django.utils.html import format_html

register = template.Library()


@register.simple_tag
def react_polls(poll):
    data = {
        'title': poll.title,
        'choices': [{
            'label': choice.label,
            'count': choice.getVoteCount()
        } for choice in poll.choices]
    }

    return format_html(
        (
            '<div id="{id}" data-poll="{poll}"></div>'
            '<script>window.adhocracy4.renderPolls("{id}")</script>'
        ),
        id='poll-' + poll.pk,
        poll=json.dumps(data)
    )

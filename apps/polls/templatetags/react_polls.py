import json

from django import template
from django.utils.html import format_html

register = template.Library()


@register.simple_tag
def react_polls():
    poll = {
        'title': (
            'Getrennte Eltern: Ist das Wechselmodell '
            'die beste Lösung für alle?'
        ),
        'choices': [{
            'label': 'Ja',
            'count': 22434
        }, {
            'label': 'Nein',
            'count': 40062
        }, {
            'label': 'Vielleicht',
            'count': 17627
        }]
    }

    return format_html(
        (
            '<div id="{id}" data-poll="{poll}"></div>'
            '<script>window.adhocracy4.renderPolls("{id}")</script>'
        ),
        id='TODO',
        poll=json.dumps(poll)
    )

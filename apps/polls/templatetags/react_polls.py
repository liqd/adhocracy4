import json

from django import template
from django.utils.html import format_html

register = template.Library()


@register.simple_tag(takes_context=True)
def react_polls(context, poll):
    user = context['request'].user
    user_choices = poll.user_choices_list(user)

    data = {
        'title': poll.title,
        'choices': [{
            'label': choice.label,
            'count': choice.vote_count,
            'ownChoice': (choice.pk in user_choices)
        } for choice in poll.choices_with_vote_count()]
    }

    return format_html(
        (
            '<div id="{id}" data-poll="{poll}"></div>'
            '<script>window.adhocracy4.renderPolls("{id}")</script>'
        ),
        id='poll-%s' % (poll.pk,),
        poll=json.dumps(data)
    )

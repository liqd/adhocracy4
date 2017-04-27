import json

from django import template
from django.utils.html import format_html

register = template.Library()


@register.simple_tag(takes_context=True)
def react_polls(context, question):
    user = context['request'].user
    user_choices = question.user_choices_list(user)

    data = {
        'label': question.label,
        'choices': [{
            'label': choice.label,
            'count': choice.vote_count,
            'ownChoice': (choice.pk in user_choices)
        } for choice in question.choices_with_vote_count()]
    }

    return format_html(
        (
            '<div id="{id}" data-question="{question}"></div>'
            '<script>window.adhocracy4.renderPolls("{id}")</script>'
        ),
        id='question-%s' % (question.pk,),
        question=json.dumps(data)
    )

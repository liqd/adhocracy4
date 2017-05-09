import json

from django import template
from django.utils.html import format_html
from rest_framework.renderers import JSONRenderer

from .. import serializers

register = template.Library()


@register.simple_tag(takes_context=True)
def react_polls(context, question):
    user = context['request'].user
    user_choices = question.user_choices_list(user)

    data = {
        'id': question.id,
        'label': question.label,
        'choices': [{
            'id': choice.id,
            'label': choice.label,
            'count': choice.vote_count,
            'ownChoice': (choice.pk in user_choices)
        } for choice in question.choices.annotate_vote_count()]
    }

    return format_html(
        (
            '<div id="{id}" data-question="{question}"></div>'
            '<script>window.adhocracy4.renderPolls("{id}")</script>'
        ),
        module=question.poll.module.pk,
        id='question-%s' % (question.pk,),
        question=json.dumps(data)
    )


@register.simple_tag
def react_poll_form(poll):
    serializer = serializers.PollSerializer(poll)
    data_poll = JSONRenderer().render(serializer.data)

    return format_html(
        (
            '<div id="{id}" data-module="{module}" data-poll="{poll}"></div>'
            '<script>window.adhocracy4.renderPollManagement("{id}")</script>'
        ),
        module=poll.module.pk,
        id='question-%s' % (poll.pk,),
        poll=data_poll
    )

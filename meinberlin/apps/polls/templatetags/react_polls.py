import json

from django import template
from django.utils.html import format_html
from rest_framework.renderers import JSONRenderer

from .. import serializers

register = template.Library()


@register.simple_tag(takes_context=True)
def react_polls(context, question):
    question_serializer = serializers.QuestionSerializer(
        question,
        context={'request': context['request']}
    )

    return format_html(
        '<div data-mb-widget="polls" data-question="{question}"></div>',
        question=JSONRenderer()
        .render(question_serializer.data)
        .decode("utf-8")
    )


@register.simple_tag
def react_poll_form(poll, reload_on_success=False):
    serializer = serializers.PollSerializer(poll)
    data_poll = JSONRenderer().render(serializer.data).decode("utf-8")
    reload_on_success = json.dumps(reload_on_success)

    return format_html(
        (
            '<div data-mb-widget="poll-management" data-module="{module}" '
            ' data-poll="{poll}"  data-reloadOnSuccess="{reload_on_success}">'
            '</div>'
        ),
        module=poll.module.pk,
        poll=data_poll,
        reload_on_success=reload_on_success,
    )

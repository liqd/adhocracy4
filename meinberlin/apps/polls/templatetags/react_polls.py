import json

from django import template
from django.utils.html import format_html
from rest_framework.renderers import JSONRenderer

from adhocracy4.rules.discovery import NormalUser

from .. import serializers

register = template.Library()


@register.simple_tag(takes_context=True)
def react_polls(context, question):
    user = context['request'].user
    user_choices = question.user_choices_list(user)
    has_poll_permission = user.has_perm(
        'meinberlin_polls.add_vote',
        question.poll.module
    )
    would_have_poll_permission = NormalUser().would_have_perm(
        'meinberlin_polls.add_vote',
        question.poll.module
    )

    data = {
        'id': question.id,
        'label': question.label,
        'isReadOnly': (not has_poll_permission and
                       not would_have_poll_permission),
        'multipleChoice': question.multiple_choice,
        'choices': [{
            'id': choice.id,
            'label': choice.label,
            'count': choice.vote_count,
            'ownChoice': (choice.pk in user_choices)
        } for choice in question.choices.annotate_vote_count()],
        'authenticated': user.is_authenticated()
    }

    return format_html(
        '<div data-mb-widget="polls" data-question="{question}"></div>',
        question=json.dumps(data)
    )


@register.simple_tag
def react_poll_form(poll, reload_on_success=False):
    serializer = serializers.PollSerializer(poll)
    data_poll = JSONRenderer().render(serializer.data)
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

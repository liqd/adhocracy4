import pytest

from adhocracy4.test.helpers import render_template


@pytest.mark.django_db
def test_react_polls(rf, user, poll):
    request = rf.get('/')
    request.user = user
    template = '{% load react_polls %}{% react_polls poll %}'
    context = {'request': request, 'poll': poll}

    rendered = render_template(template, context)

    assert rendered.startswith('<div data-a4-widget="polls" data-poll-id="')


@pytest.mark.django_db
def test_react_poll_form(poll):
    template = '{% load react_polls %}{% react_poll_form poll %}'
    context = {'poll': poll}

    rendered = render_template(template, context)

    assert rendered.startswith('<div data-a4-widget="poll-management"')

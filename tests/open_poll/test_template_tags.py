import pytest

from adhocracy4.test.helpers import render_template


@pytest.mark.django_db
def test_react_polls(rf, user, open_poll):
    request = rf.get("/")
    request.user = user
    template = "{% load react_open_poll %}{% react_open_poll open_poll %}"
    context = {"request": request, "open_poll": open_poll}

    rendered = render_template(template, context)

    assert rendered.startswith('<div data-a4-widget="open-poll"')


@pytest.mark.django_db
def test_react_poll_form(open_poll):
    template = "{% load react_open_poll %}{% react_open_poll_form open_poll %}"
    context = {"open_poll": open_poll}

    rendered = render_template(template, context)

    assert rendered.startswith('<div data-a4-widget="open-poll-management"')

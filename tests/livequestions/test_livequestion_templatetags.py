import html

import pytest
from django.urls import reverse

from adhocracy4.test.helpers import render_template


@pytest.mark.django_db
def test_react_questions(rf, user, live_question):
    request = rf.get("/")
    request.user = user
    module = live_question.module
    template = "{% load react_questions %}{% react_questions module %}"
    context = {"request": request, "module": module}

    questions_api_url = reverse("questions-list", kwargs={"module_pk": module.pk})
    present_url = reverse(
        "meinberlin_livequestions:question-present", kwargs={"module_slug": module.slug}
    )
    rendered = html.unescape(render_template(template, context))

    assert rendered.startswith('<div data-ie-widget="questions"')
    assert module.description.replace("\n", "\\n") in rendered
    assert questions_api_url in rendered
    assert present_url in rendered
    assert live_question.category.name in rendered


@pytest.mark.django_db
def test_react_questions_present(rf, user, live_question):
    request = rf.get("/")
    request.user = user
    module = live_question.module
    template = "{% load react_questions %}{% react_questions_present module %}"
    context = {"request": request, "module": module}

    questions_api_url = reverse("questions-list", kwargs={"module_pk": module.pk})
    rendered = html.unescape(render_template(template, context))

    assert rendered.startswith('<div data-ie-widget="present"')
    assert questions_api_url in rendered
    assert live_question.category.name in rendered
    assert module.project.name in rendered

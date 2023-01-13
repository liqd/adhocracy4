import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_absolute_url(live_question):
    url = reverse("module-detail", kwargs={"module_slug": live_question.module.slug})
    assert live_question.get_absolute_url() == url


@pytest.mark.django_db
def test_str(live_question):
    live_question_string = str(live_question)
    assert live_question_string == live_question.text


@pytest.mark.django_db
def test_creator_is_anonymous(live_question):
    creator = live_question.creator
    assert creator.__class__.__name__ == "AnonymousUser"
    assert str(creator) == "AnonymousUser"


@pytest.mark.django_db
def test_project(live_question):
    assert live_question.module.project == live_question.project

import pytest
from freezegun import freeze_time

from django.utils import timezone

from adhocracy4.actions.models import Action
from adhocracy4.actions.verbs import Verbs


@pytest.mark.django_db
def test_action_create(question_factory):
    question = question_factory()
    project = question.module.project
    now = timezone.now()
    with freeze_time(now):
        action = Action(
            actor=question.creator,
            verb=Verbs.ADD.value,
            obj=question,
            target=project,
            description='description'
        )
    assert action.actor == question.creator
    assert action.verb == Verbs.ADD.value
    assert action.obj == question
    assert action.target == project
    assert action.timestamp == now
    assert action.public is True
    assert action.description == 'description'


@pytest.mark.django_db
def test_action_string_full(question_factory):
    question = question_factory()
    project = question.module.project
    action = Action(
        actor=question.creator,
        verb=Verbs.ADD.value,
        obj=question,
        target=project,
    )
    str_expected = '{} add {} to {}'.format(
        question.creator,
        question,
        project
    )
    assert str(action) == str_expected


@pytest.mark.django_db
def test_action_string_with_target(question_factory):
    question = question_factory()
    project = question.module.project
    action = Action(
        verb=Verbs.ADD.value,
        obj=question,
        target=project,
    )
    str_expected = 'add {} to {}'.format(
        question,
        project
    )
    assert str(action) == str_expected


@pytest.mark.django_db
def test_action_string_with_actor(question_factory):
    question = question_factory()
    action = Action(
        actor=question.creator,
        verb=Verbs.CREATE.value,
        obj=question,
    )
    str_expected = '{} create {}'.format(
        question.creator,
        question,
    )
    assert str(action) == str_expected


@pytest.mark.django_db
def test_action_string_without_actor(question_factory):
    question = question_factory()
    action = Action(
        verb=Verbs.CREATE.value,
        obj=question,
    )
    str_expected = 'create {}'.format(
        question,
    )
    assert str(action) == str_expected

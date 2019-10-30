import pytest

from adhocracy4.actions.models import Action
from adhocracy4.actions.signals import _add_action
from adhocracy4.actions.signals import _delete_action
from adhocracy4.actions.verbs import Verbs


@pytest.mark.django_db
def test_project_create(project_factory):
    project = project_factory()
    _add_action(None, project, True, None)
    action = Action.objects.first()
    assert action.actor is None
    assert action.obj == project
    assert action.verb == Verbs.CREATE.value
    assert action.target is None


@pytest.mark.django_db
def test_item_add(question_factory):
    question = question_factory()
    _add_action(None, question, True, None)
    action = Action.objects.last()
    assert action.actor == question.creator
    assert action.obj == question
    assert action.verb == Verbs.ADD.value
    assert action.target == question.project
    assert action.project == question.project


@pytest.mark.django_db
def test_item_update(question_factory):
    question = question_factory()
    _add_action(None, question, False, None)
    action = Action.objects.last()
    assert action.actor == question.creator
    assert action.obj == question
    assert action.verb == Verbs.UPDATE.value
    assert action.target is None
    assert action.project == question.project


@pytest.mark.django_db
def test_item_delete(question_factory):
    question = question_factory()
    _add_action(question_factory._meta.model, question, False, None)
    _delete_action(question_factory._meta.model, question)
    assert Action.objects.all().count() == 0


@pytest.mark.django_db
def test_content_object_create(question_factory, comment_factory):
    question = question_factory()
    comment = comment_factory(content_object=question)
    _add_action(None, comment, True, None)
    action = Action.objects.last()
    assert action.actor == comment.creator
    assert action.obj == comment
    assert action.verb == Verbs.ADD.value
    assert action.target == question
    assert action.project == comment.project


@pytest.mark.django_db
def test_content_object_update(question_factory, comment_factory):
    question = question_factory()
    comment = comment_factory(content_object=question)
    _add_action(None, comment, False, None)
    action = Action.objects.last()
    assert action.actor == comment.creator
    assert action.obj == comment
    assert action.verb == Verbs.UPDATE.value
    assert action.target is None
    assert action.project == comment.project

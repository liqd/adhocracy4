import pytest
from django.utils import timezone
from freezegun import freeze_time

from adhocracy4.actions.models import Action
from adhocracy4.actions.models import configure_icon
from adhocracy4.actions.models import configure_type
from adhocracy4.actions.verbs import Verbs
from adhocracy4.projects.enums import Access


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


@pytest.mark.django_db
def test_type_property(question):
    action = Action(
        verb=Verbs.ADD.value,
        obj=question,
    )

    assert action.type == 'unknown'

    configure_type(
        'thing',
        (question._meta.app_label, question._meta.model_name)
    )
    assert action.type == 'thing'

    configure_type(
        'thong',
        (question._meta.app_label, question._meta.model_name)
    )
    assert action.type == 'thong'


@pytest.mark.django_db
def test_icon_property(question):
    action = Action(
        verb=Verbs.ADD.value,
        obj=question,
    )

    assert action.icon == 'star'

    configure_type(
        'thing',
        (question._meta.app_label, question._meta.model_name)
    )
    assert action.icon == 'star'

    configure_icon('plus', verb=Verbs.ADD)
    assert action.icon == 'plus'

    other_action = Action(
        verb=Verbs.CREATE.value,
        obj=question
    )
    assert other_action.icon == 'star'

    configure_icon('circle', type='thing')
    assert action.icon == 'plus'
    assert other_action.icon == 'circle'


@pytest.mark.django_db
def test_queryset_filter_public(action_factory):
    action_factory(obj__module__project__access=Access.PRIVATE)
    action_factory(obj__module__project__is_draft=True)
    action1 = action_factory(obj=None)
    action2 = action_factory(obj=None)

    assert list(Action.objects.filter_public()) == [action2, action1]


@pytest.mark.django_db
def test_queryset_exlude_update(action_factory):
    action = action_factory(verb=Verbs.UPDATE.value)
    action_factory()

    assert action not in Action.objects.exclude_updates()


@pytest.mark.django_db
def test_default_ordering(action_factory):
    action1 = action_factory()
    action2 = action_factory()
    action3 = action_factory()

    assert list(Action.objects.filter_public()) == [action3, action2, action1]

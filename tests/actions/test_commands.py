from datetime import timedelta

import pytest
from dateutil.parser import parse
from django.core.management import call_command
from freezegun import freeze_time

from adhocracy4.actions.models import Action
from adhocracy4.actions.verbs import Verbs


@pytest.mark.django_db
def test_phase_end_later(phase_factory):

    phase_factory(
        start_date=parse('2013-01-02 17:00:00 UTC'),
        end_date=parse('2013-01-02 18:00:00 UTC')
    )

    with freeze_time('2013-01-01 00:00:00 UTC'):
        call_command('create_system_actions')
        action_count = Action.objects.all().count()
        assert action_count == 0


@pytest.mark.django_db
def test_phase_end_tomorrow(phase_factory):

    phase = phase_factory(
        start_date=parse('2013-01-01 17:00:00 UTC'),
        end_date=parse('2013-01-01 18:00:00 UTC')
    )

    project = phase.module.project

    action_count = Action.objects.all().count()
    assert action_count == 0

    with freeze_time('2013-01-01 17:30:00 UTC'):
        call_command('create_system_actions')
        action_count = Action.objects.all().count()
        action = Action.objects.last()
        assert action_count == 1
        assert action.obj == phase
        assert action.verb == Verbs.SCHEDULE.value
        assert action.project == project


@pytest.mark.django_db
def test_next_phase_end_tomorrow(phase_factory):

    phase1 = phase_factory(
        start_date=parse('2013-01-01 17:00:00 UTC'),
        end_date=parse('2013-01-01 18:00:00 UTC')
    )

    phase2 = phase_factory(
        module=phase1.module,
        start_date=parse('2013-02-02 17:00:00 UTC'),
        end_date=parse('2013-02-02 18:00:00 UTC')
    )

    phase3 = phase_factory(
        module=phase1.module,
        start_date=parse('2013-02-02 18:01:00 UTC'),
        end_date=parse('2013-02-02 19:00:00 UTC')
    )

    # first phase ends within 24 h
    with freeze_time(phase1.end_date - timedelta(hours=1)):
        call_command('create_system_actions')
        action_count = Action.objects.all().count()
        assert action_count == 1

    # second phase ends within 24 h
    with freeze_time(phase2.end_date - timedelta(hours=1)):
        call_command('create_system_actions')
        action_count = Action.objects.all().count()
        assert action_count == 2

    # second phase ends within 24 h but script has already run
    with freeze_time(phase2.end_date - timedelta(hours=1)):
        call_command('create_system_actions')
        action_count = Action.objects.all().count()
        assert action_count == 2

    # third phase ends within 24 h but script has already run
    with freeze_time(phase3.start_date):
        call_command('create_system_actions')
        action_count = Action.objects.all().count()
        assert action_count == 3


@pytest.mark.django_db
def test_phase_reschedule(phase_factory):

    phase = phase_factory(
        start_date=parse('2013-01-01 17:00:00 UTC'),
        end_date=parse('2013-01-03 18:00:00 UTC')
    )

    # first phase ends within 24 h
    with freeze_time(phase.end_date - timedelta(hours=1)):
        call_command('create_system_actions')
        action_count = Action.objects.all().count()
        assert action_count == 1

    # first phases end date has been moved forward
    # and a new action will be created
    phase.end_date = phase.end_date + timedelta(days=1)
    phase.save()
    with freeze_time(phase.end_date - timedelta(hours=1)):
        call_command('create_system_actions')
        action_count = Action.objects.all().count()
        assert action_count == 2


@pytest.mark.django_db
def test_project_starts_later(phase_factory):

    phase = phase_factory(
        start_date=parse('2013-01-01 17:00:00 UTC'),
        end_date=parse('2013-01-02 18:00:00 UTC')
    )

    with freeze_time(phase.start_date - timedelta(days=1)):
        call_command('create_system_actions')
        action_count = Action.objects.all().count()
        assert action_count == 0


@pytest.mark.django_db
def test_project_start_hour(phase_factory):

    phase = phase_factory(
        start_date=parse('2013-01-01 17:00:00 UTC'),
        end_date=parse('2013-01-01 18:00:00 UTC')
    )

    phase2 = phase_factory(
        module=phase.module,
        start_date=parse('2014-01-01 17:00:00 UTC'),
        end_date=parse('2014-01-01 18:00:00 UTC')
    )

    project = phase.module.project

    action_count = Action.objects.all().count()
    assert action_count == 0

    with freeze_time(phase.start_date - timedelta(minutes=30)):
        call_command('create_system_actions')
        action_count = Action.objects.all().count()
        action = Action.objects.last()
        assert action_count == 1
        assert action.obj == project
        assert action.verb == Verbs.START.value
        assert action.project == project

    # second phase starts within an hour,
    # but that may not trigger a project start action
    with freeze_time(phase2.start_date - timedelta(minutes=30)):
        call_command('create_system_actions')
        action_count = Action.objects.all().count()
        action = Action.objects.last()
        assert action_count == 1


@pytest.mark.django_db
def test_project_start_single_action(phase_factory):

    phase = phase_factory(
        start_date=parse('2013-01-01 17:00:00 UTC'),
        end_date=parse('2013-01-01 18:00:00 UTC')
    )

    action_count = Action.objects.all().count()
    assert action_count == 0

    with freeze_time(phase.start_date - timedelta(minutes=30)):
        call_command('create_system_actions')
        action_count = Action.objects.all().count()
        assert action_count == 1

    # first phase starts within an hour but script has already run
    with freeze_time(phase.start_date - timedelta(minutes=30)):
        call_command('create_system_actions')
        action_count = Action.objects.all().count()
        assert action_count == 1


@pytest.mark.django_db
def test_project_start_reschedule(phase_factory):

    phase = phase_factory(
        start_date=parse('2013-01-01 17:00:00 UTC'),
        end_date=parse('2013-01-01 18:00:00 UTC')
    )

    # first phase starts within an hour
    with freeze_time(phase.start_date - timedelta(minutes=30)):
        call_command('create_system_actions')
        action_count = Action.objects.all().count()
        assert action_count == 1

    # first phases start date has been moved forward
    # and a new action will be created
    phase.start_date = phase.start_date + timedelta(days=1)
    phase.save()
    with freeze_time(phase.start_date - timedelta(minutes=30)):
        call_command('create_system_actions')
        action_count = Action.objects.all().count()
        assert action_count == 2

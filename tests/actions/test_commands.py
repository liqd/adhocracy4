from datetime import timedelta

import pytest
from dateutil.parser import parse
from django.core.management import call_command
from freezegun import freeze_time

from adhocracy4.actions import verbs
from adhocracy4.actions.models import Action


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
        assert action.verb == verbs.COMPLETE
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

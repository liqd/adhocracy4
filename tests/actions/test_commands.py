from datetime import timedelta

import pytest
from dateutil.parser import parse
from django.contrib.contenttypes.models import ContentType
from django.core.management import call_command
from freezegun import freeze_time

from adhocracy4.actions.models import Action
from adhocracy4.actions.verbs import Verbs
from adhocracy4.projects.models import Project

SCHEDULE = Verbs.SCHEDULE.value
START = Verbs.START.value


@pytest.mark.django_db
def test_phase_started(phase_factory):
    phase = phase_factory(
        start_date=parse("2013-01-01 17:00:00 UTC"),
        end_date=parse("2013-01-01 18:00:00 UTC"),
    )

    project = phase.module.project

    action_count = Action.objects.filter(verb=START).count()
    assert action_count == 0

    with freeze_time("2013-01-01 17:30:00 UTC"):
        call_command("create_system_actions")
        action_count = Action.objects.filter(verb=START).count()
        action_phase = Action.objects.filter(verb=START)[0]
        action_project = Action.objects.filter(verb=START)[1]

        # actions for phase and project started
        assert action_count == 2
        assert action_phase.obj == phase
        assert action_phase.verb == START
        assert action_phase.project == project
        assert action_project.obj == project
        assert action_project.verb == START


@pytest.mark.django_db
def test_phase_started_project_is_draft(phase_factory):
    phase = phase_factory(
        start_date=parse("2013-01-01 17:00:00 UTC"),
        end_date=parse("2013-01-01 18:00:00 UTC"),
    )

    project = phase.module.project
    project.is_draft = True
    project.save()
    project.refresh_from_db()

    action_count = Action.objects.filter(verb=START).count()
    assert action_count == 0

    with freeze_time("2013-01-01 17:30:00 UTC"):
        call_command("create_system_actions")
        action_count = Action.objects.filter(verb=START).count()
        assert action_count == 0


@pytest.mark.django_db
def test_draft_phase_started(phase_factory, module_factory):
    module = module_factory(is_draft=True)
    phase_factory(
        start_date=parse("2013-01-01 17:00:00 UTC"),
        end_date=parse("2013-01-01 18:00:00 UTC"),
        module=module,
    )

    action_count = Action.objects.filter(verb=START).count()
    assert action_count == 0

    with freeze_time("2013-01-01 17:30:00 UTC"):
        call_command("create_system_actions")
        action_count = Action.objects.filter(verb=START).count()
        assert action_count == 0


@pytest.mark.django_db
def test_phase_end_later(phase_factory):
    phase_factory(
        start_date=parse("2013-01-02 17:00:00 UTC"),
        end_date=parse("2013-01-02 18:00:00 UTC"),
    )

    with freeze_time("2013-01-01 00:00:00 UTC"):
        call_command("create_system_actions")
        action_count = Action.objects.filter(verb=SCHEDULE).count()
        assert action_count == 0


@pytest.mark.django_db
def test_phase_end_tomorrow(phase_factory):
    phase = phase_factory(
        start_date=parse("2013-01-01 17:00:00 UTC"),
        end_date=parse("2013-01-01 18:00:00 UTC"),
    )

    project = phase.module.project

    action_count = Action.objects.filter(verb=SCHEDULE).count()
    assert action_count == 0

    with freeze_time("2013-01-01 17:30:00 UTC"):
        call_command("create_system_actions")
        action_count = Action.objects.filter(verb=SCHEDULE).count()
        action = Action.objects.filter(verb=SCHEDULE).last()
        assert action_count == 1
        assert action.obj == phase
        assert action.verb == SCHEDULE
        assert action.project == project


@pytest.mark.django_db
def test_phase_end_tomorrow_project_is_draft(phase_factory):
    phase = phase_factory(
        start_date=parse("2013-01-01 17:00:00 UTC"),
        end_date=parse("2013-01-01 18:00:00 UTC"),
    )

    project = phase.module.project
    project.is_draft = True
    project.save()
    project.refresh_from_db()

    action_count = Action.objects.filter(verb=SCHEDULE).count()
    assert action_count == 0

    with freeze_time("2013-01-01 17:30:00 UTC"):
        call_command("create_system_actions")
        action_count = Action.objects.filter(verb=SCHEDULE).count()
        assert action_count == 0


@pytest.mark.django_db
def test_draft_phase_end_tomorrow(phase_factory, module_factory):
    module = module_factory(is_draft=True)
    phase_factory(
        start_date=parse("2013-01-01 17:00:00 UTC"),
        end_date=parse("2013-01-01 18:00:00 UTC"),
        module=module,
    )

    action_count = Action.objects.filter(verb=SCHEDULE).count()
    assert action_count == 0

    with freeze_time("2013-01-01 17:30:00 UTC"):
        call_command("create_system_actions")
        action_count = Action.objects.filter(verb=SCHEDULE).count()
        assert action_count == 0


@pytest.mark.django_db
def test_next_phase_end_tomorrow(phase_factory):
    phase1 = phase_factory(
        start_date=parse("2013-01-01 17:00:00 UTC"),
        end_date=parse("2013-01-01 18:00:00 UTC"),
    )

    phase2 = phase_factory(
        module=phase1.module,
        start_date=parse("2013-02-02 17:00:00 UTC"),
        end_date=parse("2013-02-02 18:00:00 UTC"),
    )

    phase3 = phase_factory(
        module=phase1.module,
        start_date=parse("2013-02-02 18:01:00 UTC"),
        end_date=parse("2013-02-02 19:00:00 UTC"),
    )

    # first phase ends within 24 h
    with freeze_time(phase1.end_date - timedelta(hours=1)):
        call_command("create_system_actions")
        action_count = Action.objects.filter(verb=SCHEDULE).count()
        assert action_count == 1

    # second phase ends within 24 h
    with freeze_time(phase2.end_date - timedelta(hours=1)):
        call_command("create_system_actions")
        action_count = Action.objects.filter(verb=SCHEDULE).count()
        assert action_count == 2

    # second phase ends within 24 h but script has already run
    with freeze_time(phase2.end_date - timedelta(hours=1)):
        call_command("create_system_actions")
        action_count = Action.objects.filter(verb=SCHEDULE).count()
        assert action_count == 2

    # third phase ends within 24 h but script has already run
    with freeze_time(phase3.start_date):
        call_command("create_system_actions")
        action_count = Action.objects.filter(verb=SCHEDULE).count()
        assert action_count == 3


@pytest.mark.django_db
def test_phase_reschedule(phase_factory):
    phase = phase_factory(
        start_date=parse("2013-01-01 17:00:00 UTC"),
        end_date=parse("2013-01-03 18:00:00 UTC"),
    )

    # first phase ends within 24 h
    with freeze_time(phase.end_date - timedelta(hours=1)):
        call_command("create_system_actions")
        action_count = Action.objects.filter(verb=SCHEDULE).count()
        assert action_count == 1

    # first phases end date has been moved forward
    # and a new action will be created
    phase.end_date = phase.end_date + timedelta(days=1)
    phase.save()
    with freeze_time(phase.end_date - timedelta(hours=1)):
        call_command("create_system_actions")
        action_count = Action.objects.filter(verb=SCHEDULE).count()
        assert action_count == 2


@pytest.mark.django_db
def test_project_starts_later_or_earlier(phase_factory):
    phase = phase_factory(
        start_date=parse("2013-01-01 17:00:00 UTC"),
        end_date=parse("2013-01-02 18:00:00 UTC"),
    )

    with freeze_time(phase.start_date - timedelta(days=1)):
        call_command("create_system_actions")
        action_count = Action.objects.filter(verb=START).count()
        assert action_count == 0

    with freeze_time(phase.start_date + timedelta(days=1)):
        call_command("create_system_actions")
        action_count = Action.objects.filter(verb=START).count()
        assert action_count == 0


@pytest.mark.django_db
def test_project_start_last_hour(phase_factory):
    phase = phase_factory(
        start_date=parse("2013-01-01 17:00:00 UTC"),
        end_date=parse("2013-01-01 18:00:00 UTC"),
    )

    phase2 = phase_factory(
        module=phase.module,
        start_date=parse("2014-01-01 17:00:00 UTC"),
        end_date=parse("2014-01-01 18:00:00 UTC"),
    )

    project = phase.module.project
    content_type = ContentType.objects.get_for_model(Project)

    action_count = Action.objects.filter(
        verb=START, obj_content_type=content_type
    ).count()
    assert action_count == 0

    with freeze_time(phase.start_date + timedelta(minutes=30)):
        call_command("create_system_actions")
        action_count = Action.objects.filter(
            verb=START, obj_content_type=content_type
        ).count()
        action = Action.objects.filter(verb=START, obj_content_type=content_type).last()
        assert action_count == 1
        assert action.obj == project
        assert action.verb == START
        assert action.project == project

    # second phase starts within the last hour,
    # but that may not trigger a project start action
    with freeze_time(phase2.start_date + timedelta(minutes=30)):
        call_command("create_system_actions")
        action_count = Action.objects.filter(
            verb=START, obj_content_type=content_type
        ).count()
        assert action_count == 1


@pytest.mark.django_db
def test_project_start_single_action(phase_factory):
    phase = phase_factory(
        start_date=parse("2013-01-01 17:00:00 UTC"),
        end_date=parse("2013-01-01 18:00:00 UTC"),
    )

    content_type = ContentType.objects.get_for_model(Project)

    action_count = Action.objects.filter(
        verb=START, obj_content_type=content_type
    ).count()
    assert action_count == 0

    with freeze_time(phase.start_date + timedelta(minutes=30)):
        call_command("create_system_actions")
        action_count = Action.objects.filter(
            verb=START, obj_content_type=content_type
        ).count()
        assert action_count == 1

    # first phase starts within the last hour but script has already run
    with freeze_time(phase.start_date + timedelta(minutes=45)):
        call_command("create_system_actions")
        action_count = Action.objects.filter(
            verb=START, obj_content_type=content_type
        ).count()
        assert action_count == 1


@pytest.mark.django_db
def test_project_start_reschedule(phase_factory):
    phase = phase_factory(
        start_date=parse("2013-01-01 17:00:00 UTC"),
        end_date=parse("2013-01-01 18:00:00 UTC"),
    )

    content_type = ContentType.objects.get_for_model(Project)

    # first phase starts within an hour
    with freeze_time(phase.start_date + timedelta(minutes=30)):
        call_command("create_system_actions")
        action_count = Action.objects.filter(
            verb=START, obj_content_type=content_type
        ).count()
        assert action_count == 1

    # first phases start date has been moved forward
    # and the start actions timestamp has to be adapted
    phase.start_date = phase.start_date + timedelta(days=1)
    phase.save()
    with freeze_time(phase.start_date + timedelta(minutes=30)):
        call_command("create_system_actions")
        action_count = Action.objects.filter(
            verb=START, obj_content_type=content_type
        ).count()
        assert action_count == 1
        action = Action.objects.filter(
            verb=START, obj_content_type=content_type
        ).first()
        assert action.timestamp == phase.start_date


@pytest.mark.django_db
def test_project_start_multi_module(phase_factory, module_factory, project):
    module1 = module_factory(weight=1, project=project)
    module2 = module_factory(weight=2, project=project)

    # phase is after phase2, but is in a module with lower weight
    phase = phase_factory(
        module=module1,
        start_date=parse("2022-01-20 17:00:00 UTC"),
        end_date=parse("2022-01-24 18:00:00 UTC"),
    )

    phase2 = phase_factory(
        module=module2,
        start_date=parse("2022-01-15 17:00:00 UTC"),
        end_date=parse("2022-01-19 18:00:00 UTC"),
    )
    content_type = ContentType.objects.get_for_model(Project)

    action_count = Action.objects.filter(
        verb=START, obj_content_type=content_type
    ).count()
    assert action_count == 0

    # first phase in list starts after second phase, should not
    # create action project start
    with freeze_time(phase.start_date + timedelta(minutes=30)):
        call_command("create_system_actions")
        action_count = Action.objects.filter(
            verb=START, obj_content_type=content_type
        ).count()

        assert action_count == 0

    # second phase in list is first phase timewise, should create action
    with freeze_time(phase2.start_date + timedelta(minutes=30)):
        call_command("create_system_actions")
        action_count = Action.objects.filter(
            verb=START, obj_content_type=content_type
        ).count()
        action = Action.objects.filter(verb=START, obj_content_type=content_type).last()
        assert action_count == 1
        assert action.obj == project
        assert action.verb == START
        assert action.project == project
        assert action.timestamp == phase2.start_date

from datetime import timedelta

import pytest
from dateutil.parser import parse
from freezegun import freeze_time

from adhocracy4.projects import models


@pytest.mark.django_db
def test_days_left(project_factory, phase_factory):
    project1 = project_factory()
    project2 = project_factory()
    phase1 = phase_factory(
        start_date=parse('2013-01-01 18:00:00 UTC'),
        end_date=parse('2013-01-02 18:00:00 UTC'),
        module__project=project1,
    )
    phase2 = phase_factory(
        start_date=parse('2013-02-01 18:00:00 UTC'),
        end_date=parse('2013-02-02 18:00:00 UTC'),
        module__project=project2,
    )

    with freeze_time(phase1.start_date):
        assert project1.days_left == 1
        del project1.days_left
    with freeze_time(phase1.end_date):
        assert project1.days_left == 0
        del project1.days_left
    with freeze_time(phase2.start_date):
        assert project2.days_left == 1
        del project2.days_left
    with freeze_time(phase2.end_date):
        assert project2.days_left == 0


@pytest.mark.django_db
def test_has_started(phase):
    project = phase.module.project
    with freeze_time(phase.start_date - timedelta(minutes=1)):
        assert not project.has_started
        del project.has_started
    with freeze_time(phase.start_date):
        assert project.has_started


@pytest.mark.django_db
def test_has_finished(project, phase_factory):
    phase1 = phase_factory(
        start_date=parse('2013-01-01 18:00:00 UTC'),
        end_date=parse('2013-01-02 18:00:00 UTC'),
        module__project=project,
    )
    phase2 = phase_factory(
        start_date=parse('2013-02-01 18:00:00 UTC'),
        end_date=parse('2013-02-02 18:00:00 UTC'),
        module__project=project,
    )

    with freeze_time(phase1.start_date - timedelta(minutes=1)):
        assert not project.has_finished
        del project.has_finished
    with freeze_time(phase1.start_date):
        assert not project.has_finished
        del project.has_finished
    with freeze_time(phase1.end_date):
        assert not project.has_finished
        del project.has_finished
    with freeze_time(phase2.end_date):
        assert project.has_finished


@pytest.mark.django_db
def test_phases_property(module, phase_factory):
    project = module.project
    phase1 = phase_factory(module=module, type='fake:30:type', weight=30)
    phase2 = phase_factory(module=module, type='fake:20:type', weight=20)

    assert list(project.phases) == [phase2, phase1]


@pytest.mark.django_db
def test_active_phase_property(project, module_factory, phase_factory):
    module1 = module_factory(project=project, weight=1)
    module2 = module_factory(project=project, weight=2)
    phase1 = phase_factory(
        module=module1,
        start_date=parse('2013-01-01 18:00:00 UTC'),
        end_date=parse('2013-01-10 18:00:00 UTC'),
        weight=1,
    )
    phase2 = phase_factory(
        module=module2,
        start_date=parse('2013-01-05 18:00:00 UTC'),
        end_date=parse('2013-01-15 18:00:00 UTC'),
        weight=1,
    )
    phase3 = phase_factory(
        module=module2,
        start_date=parse('2013-03-01 18:00:00 UTC'),
        end_date=parse('2013-03-02 18:00:00 UTC'),
        weight=2,
    )

    # Freeze prior to every phase
    with freeze_time(phase1.start_date - timedelta(minutes=1)):
        assert project.active_phase is None
        del project.active_phase
    # Freeze during single phase
    with freeze_time(phase1.start_date):
        project = models.Project.objects.get(id=project.id)
        assert project.active_phase == phase1
        del project.active_phase
    # Freeze overlapping phases from different modules
    with freeze_time(phase2.start_date):
        project = models.Project.objects.get(id=project.id)
        assert project.active_phase == phase2
        del project.active_phase
    # Freeze single phase from overlapping modules
    with freeze_time(phase2.end_date - timedelta(minutes=1)):
        project = models.Project.objects.get(id=project.id)
        assert project.active_phase == phase2
        del project.active_phase
    # Freeze on gap between phases of a module
    with freeze_time(phase3.start_date - timedelta(minutes=1)):
        project = models.Project.objects.get(id=project.id)
        assert project.active_phase is None
        del project.active_phase
    # Freeze after every phase
    with freeze_time(phase3.end_date):
        project = models.Project.objects.get(id=project.id)
        assert project.active_phase is None
        del project.active_phase


@pytest.mark.django_db
def test_last_active_phase_property(project, module_factory, phase_factory):
    module1 = module_factory(project=project, weight=1)
    module2 = module_factory(project=project, weight=2)
    phase1 = phase_factory(
        module=module1,
        start_date=parse('2013-01-01 18:00:00 UTC'),
        end_date=parse('2013-01-10 18:00:00 UTC'),
        weight=1,
    )
    phase2 = phase_factory(
        module=module2,
        start_date=parse('2013-01-05 18:00:00 UTC'),
        end_date=parse('2013-01-15 18:00:00 UTC'),
        weight=1,
    )
    phase3 = phase_factory(
        module=module1,
        start_date=parse('2013-01-11 18:00:00 UTC'),
        end_date=parse('2013-01-12 18:00:00 UTC'),
        weight=2,
    )
    phase4 = phase_factory(
        module=module2,
        start_date=parse('2013-03-01 18:00:00 UTC'),
        end_date=parse('2013-03-02 18:00:00 UTC'),
        weight=2,
    )

    # Freeze prior to every phase
    with freeze_time(phase1.start_date - timedelta(minutes=1)):
        assert project.last_active_phase is None
        del project.last_active_phase
    # Freeze during single phase
    with freeze_time(phase1.start_date):
        project = models.Project.objects.get(id=project.id)
        assert project.last_active_phase == phase1
    # Freeze overlapping phases from different modules
    with freeze_time(phase2.start_date):
        project = models.Project.objects.get(id=project.id)
        assert project.last_active_phase == phase2
    # Freeze overlapping phases from different modules
    with freeze_time(phase3.start_date):
        project = models.Project.objects.get(id=project.id)
        assert project.last_active_phase == phase3
    # Freeze single phase that started before another enclosed phase
    with freeze_time(phase3.end_date - timedelta(minutes=1)):
        project = models.Project.objects.get(id=project.id)
        assert project.last_active_phase == phase3
    # Freeze on gap between phases of a module
    with freeze_time(phase4.start_date - timedelta(minutes=1)):
        project = models.Project.objects.get(id=project.id)
        assert project.last_active_phase == phase3
    # Freeze after every phase
    with freeze_time(phase4.end_date):
        project = models.Project.objects.get(id=project.id)
        assert project.last_active_phase == phase4


@pytest.mark.django_db
def test_last_active_module_property(project, module_factory, phase_factory):
    module1 = module_factory(project=project, weight=1)
    module2 = module_factory(project=project, weight=2)
    phase1 = phase_factory(
        module=module1,
        start_date=parse('2013-01-01 18:00:00 UTC'),
        end_date=parse('2013-01-10 18:00:00 UTC'),
        weight=1,
    )
    phase2 = phase_factory(
        module=module2,
        start_date=parse('2013-01-05 18:00:00 UTC'),
        end_date=parse('2013-01-15 18:00:00 UTC'),
        weight=1,
    )
    phase3 = phase_factory(
        module=module1,
        start_date=parse('2013-01-11 18:00:00 UTC'),
        end_date=parse('2013-01-12 18:00:00 UTC'),
        weight=2,
    )
    phase4 = phase_factory(
        module=module2,
        start_date=parse('2013-03-01 18:00:00 UTC'),
        end_date=parse('2013-03-02 18:00:00 UTC'),
        weight=2,
    )

    # Freeze prior to every phase
    with freeze_time(phase1.start_date - timedelta(minutes=1)):
        assert project.last_active_module is None
    # Freeze during single phase
    with freeze_time(phase1.start_date):
        project = models.Project.objects.get(id=project.id)
        assert project.last_active_module == module1
        del project.last_active_module
    # Freeze overlapping phases from different modules
    with freeze_time(phase2.start_date):
        project = models.Project.objects.get(id=project.id)
        assert project.last_active_module == module2
        del project.last_active_module
    # Freeze overlapping phases from different modules
    with freeze_time(phase3.start_date):
        project = models.Project.objects.get(id=project.id)
        assert project.last_active_module == module1
        del project.last_active_module
    # Freeze single phase from overlapping modules
    with freeze_time(phase3.end_date - timedelta(minutes=1)):
        project = models.Project.objects.get(id=project.id)
        assert project.last_active_module == module1
        del project.last_active_module
    # Freeze on gap between phases of a module
    with freeze_time(phase4.start_date - timedelta(minutes=1)):
        project = models.Project.objects.get(id=project.id)
        assert project.last_active_module == module1
        del project.last_active_module
    # Freeze after every phase
    with freeze_time(phase4.end_date):
        project = models.Project.objects.get(id=project.id)
        assert project.last_active_module == module2
        del project.last_active_module


@pytest.mark.django_db
def test_active_phase_ends_next(project, module_factory, phase_factory):
    module1 = module_factory(project=project, weight=1)
    module2 = module_factory(project=project, weight=2)
    phase_factory(
        module=module1,
        start_date=parse('2013-01-01 17:00:00 UTC'),
        end_date=parse('2013-01-01 18:05:00 UTC')
    )
    phase2 = phase_factory(
        module=module2,
        start_date=parse('2013-01-01 17:05:00 UTC'),
        end_date=parse('2013-01-01 18:00:00 UTC')
    )
    with freeze_time('2013-01-01 17:30:00 UTC'):
        assert project.active_phase_ends_next == phase2


@pytest.mark.django_db
def test_time_left_plural(project, module_factory, phase_factory):
    module1 = module_factory(project=project, weight=1)
    module2 = module_factory(project=project, weight=2)
    phase_factory(
        module=module1,
        start_date=parse('2013-01-01 17:00:00 UTC'),
        end_date=parse('2013-01-01 18:05:00 UTC')
    )
    phase_factory(
        module=module2,
        start_date=parse('2013-01-01 17:05:00 UTC'),
        end_date=parse('2013-01-01 18:00:00 UTC')
    )
    with freeze_time('2013-01-01 17:30:00 UTC'):
        assert project.time_left == '30 minutes'


@pytest.mark.django_db
def test_time_left_singular(project, module_factory, phase_factory):
    module1 = module_factory(project=project, weight=1)
    phase_factory(
        module=module1,
        start_date=parse('2013-01-01 16:00:00 UTC'),
        end_date=parse('2013-01-01 18:00:00 UTC')
    )
    with freeze_time('2013-01-01 17:00:00 UTC'):
        assert project.time_left == '1 hour'


@pytest.mark.django_db
def test_time_left_seconds(project, module_factory, phase_factory):
    module1 = module_factory(project=project, weight=1)
    phase_factory(
        module=module1,
        start_date=parse('2013-01-01 16:00:00 UTC'),
        end_date=parse('2013-01-01 18:00:00 UTC')
    )
    with freeze_time('2013-01-01 17:59:22 UTC'):
        assert project.time_left == '38 seconds'


@pytest.mark.django_db
def test_time_left_0_seconds(project, module_factory, phase_factory):
    module1 = module_factory(project=project, weight=1)
    phase_factory(
        module=module1,
        start_date=parse('2013-01-01 16:00:00 UTC'),
        end_date=parse('2013-01-01 18:00:00.45 UTC')
    )
    with freeze_time('2013-01-01 18:00:00 UTC'):
        assert project.time_left == '0 seconds'


@pytest.mark.django_db
def test_active_phase_progress(project, module_factory, phase_factory):
    module1 = module_factory(project=project, weight=1)
    module2 = module_factory(project=project, weight=2)
    phase_factory(
        module=module1,
        start_date=parse('2013-01-01 17:00:00 UTC'),
        end_date=parse('2013-01-01 18:05:00 UTC')
    )
    phase_factory(
        module=module2,
        start_date=parse('2013-01-01 17:05:00 UTC'),
        end_date=parse('2013-01-01 18:00:00 UTC')
    )
    with freeze_time('2013-01-01 17:30:00 UTC'):
        assert project.active_phase_progress == 45


@pytest.mark.django_db
def test_active_phase_progress_no_active_phase(
        project, module_factory, phase_factory):
    module1 = module_factory(project=project, weight=1)
    phase_factory(
        module=module1,
        start_date=parse('2013-01-01 17:00:00 UTC'),
        end_date=parse('2013-01-01 18:05:00 UTC')
    )
    with freeze_time('2013-01-01 18:30:00 UTC'):
        assert project.active_phase_progress is None


@pytest.mark.django_db
def test_future_phases(project, module_factory, phase_factory):
    module1 = module_factory(project=project, weight=1)
    module2 = module_factory(project=project, weight=2)
    phase1 = phase_factory(
        module=module1,
        start_date=parse('2013-01-01 17:00:00 UTC'),
        end_date=parse('2013-01-01 18:05:00 UTC')
    )
    phase2 = phase_factory(
        module=module2,
        start_date=parse('2013-01-01 17:05:00 UTC'),
        end_date=parse('2013-01-01 18:00:00 UTC')
    )
    phase3 = phase_factory(
        module=module1,
        start_date=parse('2013-01-01 19:00:00 UTC'),
        end_date=parse('2013-01-01 20:05:00 UTC')
    )
    phase4 = phase_factory(
        module=module2,
        start_date=parse('2013-01-01 19:05:00 UTC'),
        end_date=parse('2013-01-01 20:00:00 UTC')
    )
    with freeze_time('2013-01-01 18:30:00 UTC'):
        assert phase1 not in project.future_phases
        assert phase2 not in project.future_phases
        assert phase3 in project.future_phases
        assert phase4 in project.future_phases


@pytest.mark.django_db
def test_past_phases(project, module_factory, phase_factory):
    module1 = module_factory(project=project, weight=1)
    module2 = module_factory(project=project, weight=2)
    phase1 = phase_factory(
        module=module1,
        start_date=parse('2013-01-01 17:00:00 UTC'),
        end_date=parse('2013-01-01 18:05:00 UTC')
    )
    phase2 = phase_factory(
        module=module2,
        start_date=parse('2013-01-01 17:05:00 UTC'),
        end_date=parse('2013-01-01 18:00:00 UTC')
    )
    phase3 = phase_factory(
        module=module1,
        start_date=parse('2013-01-01 19:00:00 UTC'),
        end_date=parse('2013-01-01 20:05:00 UTC')
    )
    phase4 = phase_factory(
        module=module2,
        start_date=parse('2013-01-01 19:05:00 UTC'),
        end_date=parse('2013-01-01 20:00:00 UTC')
    )
    with freeze_time('2013-01-01 19:00:00 UTC'):
        assert phase1 in project.past_phases
        assert phase2 in project.past_phases
        assert phase3 not in project.past_phases
        assert phase4 not in project.past_phases


@pytest.mark.django_db
def test_end_date(project_factory, phase_factory):

    phase = phase_factory(start_date=None, end_date=None)
    assert not phase.module.project.end_date

    module = phase.module

    phase_factory(
        module=module,
        end_date=parse('2013-01-01 20:00:00 UTC'))
    del module.project.end_date

    assert str(module.project.end_date) == '2013-01-01 20:00:00+00:00'

from datetime import timedelta

import pytest
from dateutil.parser import parse
from freezegun import freeze_time


@pytest.mark.django_db
def test_str(module):
    assert str(module) == \
        "{} ({})".format(module.project, module.weight)


@pytest.mark.django_db
def test_phases(phase, phase_factory):
    module = phase.module
    phase2 = phase_factory(module=module)
    assert list(module.phases) == [phase, phase2]


@pytest.mark.django_db
def test_active_phase(phase_factory):
    phase1 = phase_factory()
    phase2 = phase_factory()
    with freeze_time(phase1.start_date):
        module1 = phase1.module
        assert module1.active_phase == phase1
    with freeze_time(phase2.start_date - timedelta(days=1)):
        module2 = phase2.module
        assert module2.active_phase is None


@pytest.mark.django_db
def test_future_phases(phase_factory):
    phase1 = phase_factory(
        start_date=parse('2013-01-01 17:00:00 UTC'),
        end_date=parse('2013-01-01 18:00:00 UTC')
    )
    module1 = phase1.module
    phase2 = phase_factory(
        start_date=parse('2013-01-01 17:00:00 UTC'),
        end_date=parse('2013-01-01 18:00:00 UTC')
    )
    module2 = phase2.module
    phase3 = phase_factory(
        module=module2,
        start_date=parse('2013-01-01 18:00:00 UTC'),
        end_date=parse('2013-01-01 18:00:01 UTC')
    )
    with freeze_time('2013-01-01 16:00:00 UTC'):
        assert phase1 in module1.future_phases
        assert phase2 not in module1.future_phases
        assert phase3 not in module1.future_phases
        assert phase1 not in module2.future_phases
        assert phase2 in module2.future_phases
        assert phase3 in module2.future_phases


@pytest.mark.django_db
def test_last_active_phase(module, phase_factory):
    phase1 = phase_factory(
        module=module,
        start_date=parse('2013-01-01 18:00:00 UTC'),
        end_date=parse('2013-01-02 18:00:00 UTC'),
    )
    phase2 = phase_factory(
        module=module,
        start_date=parse('2013-02-01 18:00:00 UTC'),
        end_date=parse('2013-02-02 18:00:00 UTC'),
    )

    with freeze_time(phase1.start_date - timedelta(minutes=1)):
        assert module.last_active_phase is None

    # reinitialize module object
    module = module.__class__.objects.get(pk=module.pk)

    with freeze_time(phase1.start_date):
        assert module.last_active_phase == phase1

    module = module.__class__.objects.get(pk=module.pk)
    with freeze_time(phase1.end_date):
        assert module.last_active_phase == phase1

    module = module.__class__.objects.get(pk=module.pk)
    with freeze_time(phase2.end_date):
        assert module.last_active_phase == phase2


@pytest.mark.django_db
def test_first_phase_start_date(phase, phase_factory):
    module = phase.module
    first_phase = phase_factory(
        module=module, start_date=phase.start_date - timedelta(days=1))
    assert module.first_phase_start_date == first_phase.start_date


@pytest.mark.django_db
def test_module_dates(phase_factory):
    phase1 = phase_factory(
        start_date=parse('2013-01-01 17:00:00 UTC'),
        end_date=parse('2013-01-01 18:00:00 UTC')
    )
    module1 = phase1.module
    phase2 = phase_factory(
        start_date=parse('2013-01-01 17:00:00 UTC'),
        end_date=parse('2013-01-01 18:00:00 UTC')
    )
    module2 = phase2.module
    phase_factory(
        module=module2,
        start_date=parse('2013-01-01 18:00:01 UTC'),
        end_date=parse('2013-01-01 19:00:00 UTC')
    )
    phase_factory(
        module=module2,
        start_date=parse('2013-01-01 19:00:01 UTC'),
        end_date=parse('2013-01-01 20:00:00 UTC')
    )

    assert module1.module_start == parse('2013-01-01 17:00:00 UTC')
    assert module1.module_end == parse('2013-01-01 18:00:00 UTC')
    assert module2.module_start == parse('2013-01-01 17:00:00 UTC')
    assert module2.module_end == parse('2013-01-01 20:00:00 UTC')


@pytest.mark.django_db
def test_module_has_started(phase_factory):
    phase1 = phase_factory(
        start_date=parse('2013-01-01 17:02:00 UTC'),
        end_date=parse('2013-01-01 18:00:00 UTC')
    )
    module1 = phase1.module
    phase2 = phase_factory(
        start_date=parse('2013-01-01 17:00:00 UTC'),
        end_date=parse('2013-01-01 18:00:00 UTC')
    )
    module2 = phase2.module
    phase_factory(
        module=module2,
        start_date=parse('2013-01-01 18:00:01 UTC'),
        end_date=parse('2013-01-01 19:00:00 UTC')
    )
    with freeze_time('2013-01-01 17:00:00 UTC'):
        assert not module1.module_has_started
        assert module2.module_has_started


@pytest.mark.django_db
def test_module_has_finished(phase_factory):
    phase1 = phase_factory(
        start_date=parse('2013-01-01 17:02:00 UTC'),
        end_date=parse('2013-01-01 18:00:00 UTC')
    )
    module1 = phase1.module
    phase2 = phase_factory(
        start_date=parse('2013-01-01 17:00:00 UTC'),
        end_date=parse('2013-01-01 18:00:00 UTC')
    )
    module2 = phase2.module
    phase_factory(
        module=module2,
        start_date=parse('2013-01-01 18:00:01 UTC'),
        end_date=parse('2013-01-01 19:00:00 UTC')
    )
    with freeze_time('2013-01-01 18:02:00 UTC'):
        assert module1.module_has_finished
        assert not module2.module_has_finished


@pytest.mark.django_db
def test_module_starting_time_left(phase_factory):
    phase1 = phase_factory(
        start_date=parse('2021-05-12 17:35:00 UTC'),
        end_date=parse('2021-05-13 18:01:00 UTC')
    )
    module1 = phase1.module
    phase2 = phase_factory(
        start_date=parse('2021-05-12 17:35:00 UTC'),
        end_date=parse('2021-05-13 18:01:00 UTC')
    )
    module2 = phase2.module
    phase_factory(
        module=module2,
        start_date=parse('2021-05-11 17:20:01 UTC'),
        end_date=parse('2021-05-12 17:20:00 UTC')
    )
    phase3 = phase_factory(
        start_date=parse('2021-05-11 20:00:00 UTC'),
        end_date=parse('2021-05-13 17:20:00 UTC')
    )
    module3 = phase3.module
    phase4 = phase_factory(
        start_date=parse('2021-05-11 17:20:00.45 UTC'),
        end_date=parse('2021-05-14 17:20:00 UTC')
    )
    module4 = phase4.module
    # with active phase
    phase5 = phase_factory(
        start_date=parse('2021-05-11 17:00:00 UTC'),
        end_date=parse('2021-05-14 17:20:00 UTC')
    )
    module5 = phase5.module
    # with past phase
    phase6 = phase_factory(
        start_date=parse('2021-05-10 17:20:00 UTC'),
        end_date=parse('2021-05-11 17:00:00 UTC')
    )
    module6 = phase6.module
    # between two phases
    phase7 = phase_factory(
        start_date=parse('2021-05-10 17:20:00 UTC'),
        end_date=parse('2021-05-11 17:00:00 UTC')
    )
    module7 = phase7.module
    phase_factory(
        module=module7,
        start_date=parse('2021-05-11 17:20:01 UTC'),
        end_date=parse('2021-05-12 17:20:00 UTC')
    )
    with freeze_time('2021-05-11 17:20:00 UTC'):
        assert module1.module_starting_time_left \
            == '1 day'
        assert module2.module_starting_time_left \
            == '1 second'
        assert module3.module_starting_time_left \
            == '2 hours'
        assert module4.module_starting_time_left \
            == '0 seconds'
        assert module5.module_starting_time_left is None
        assert module6.module_starting_time_left is None
        assert module7.module_starting_time_left is None


@pytest.mark.django_db
def test_module_running_time_left(phase_factory):
    phase1 = phase_factory(
        start_date=parse('2013-01-01 17:00:00 UTC'),
        end_date=parse('2013-01-02 18:01:00 UTC')
    )
    module1 = phase1.module
    phase2 = phase_factory(
        start_date=parse('2013-01-01 17:00:00 UTC'),
        end_date=parse('2013-01-01 18:00:00 UTC')
    )
    module2 = phase2.module
    phase_factory(
        module=module2,
        start_date=parse('2013-01-01 18:00:00 UTC'),
        end_date=parse('2013-01-01 18:00:01 UTC')
    )
    phase3 = phase_factory(
        start_date=parse('2013-01-01 17:00:00 UTC'),
        end_date=parse('2013-01-01 19:00:00 UTC')
    )
    module3 = phase3.module
    phase_factory(
        module=module3,
        start_date=parse('2013-01-01 19:00:01 UTC'),
        end_date=parse('2013-01-01 20:00:00 UTC')
    )
    phase4 = phase_factory(
        start_date=parse('2013-01-01 17:00:00 UTC'),
        end_date=parse('2013-01-01 18:00:00.45 UTC')
    )
    module4 = phase4.module
    # with future phase
    phase5 = phase_factory(
        start_date=parse('2013-05-11 17:00:00 UTC'),
        end_date=parse('2013-05-14 17:20:00 UTC')
    )
    module5 = phase5.module
    # with past phase
    phase6 = phase_factory(
        start_date=parse('2013-01-01 8:00:00 UTC'),
        end_date=parse('2013-01-01 17:00:00 UTC')
    )
    module6 = phase6.module
    # between two phases
    phase7 = phase_factory(
        start_date=parse('2013-01-01 8:00:00 UTC'),
        end_date=parse('2013-01-01 17:00:00 UTC')
    )
    module7 = phase7.module
    phase_factory(
        module=module7,
        start_date=parse('2013-01-01 18:30:00 UTC'),
        end_date=parse('2013-01-01 21:00:00 UTC')
    )
    with freeze_time('2013-01-01 18:00:00 UTC'):
        assert module1.module_running_time_left \
            == '1 day'
        assert module2.module_running_time_left \
            == '1 second'
        assert module3.module_running_time_left \
            == '2 hours'
        assert module4.module_running_time_left \
            == '0 seconds'
        assert module5.module_running_time_left is None
        assert module6.module_running_time_left is None
        assert module7.module_running_time_left \
            == '3 hours'


@pytest.mark.django_db
def test_module_running_progress(phase_factory):
    phase1 = phase_factory(
        start_date=parse('2013-01-01 17:00:00 UTC'),
        end_date=parse('2013-01-01 18:00:00 UTC')
    )
    module1 = phase1.module
    phase2 = phase_factory(
        start_date=parse('2013-01-01 17:00:00 UTC'),
        end_date=parse('2013-01-01 18:00:00 UTC')
    )
    module2 = phase2.module
    phase_factory(
        module=module2,
        start_date=parse('2013-01-01 18:00:00 UTC'),
        end_date=parse('2013-01-02 18:00:01 UTC')
    )
    phase4 = phase_factory(
        start_date=parse('2013-01-01 17:00:00 UTC'),
        end_date=parse('2013-01-01 19:00:00 UTC')
    )
    module3 = phase4.module
    phase_factory(
        module=module3,
        start_date=parse('2013-01-01 19:00:01 UTC'),
        end_date=parse('2013-01-01 20:00:00 UTC')
    )
    with freeze_time('2013-01-01 17:30:00 UTC'):
        assert module1.module_running_progress == 50
        assert module2.module_running_progress == 2
        assert module3.module_running_progress == 17

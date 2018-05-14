from datetime import timedelta
from dateutil.parser import parse
import pytest
from freezegun import freeze_time


@pytest.mark.django_db
def test_active_phase(phase):
    module = phase.module
    with freeze_time(phase.start_date):
        assert module.active_phase == phase
    with freeze_time(phase.start_date - timedelta(days=1)):
        assert module.active_phase is None


@pytest.mark.django_db
def test_first_phase_start_date(phase, phase_factory):
    module = phase.module
    first_phase = phase_factory(
        module=module, start_date=phase.start_date - timedelta(days=1))
    assert module.first_phase_start_date == first_phase.start_date


@pytest.mark.django_db
def test_phases(phase, phase_factory):
    module = phase.module
    phase2 = phase_factory(module=module)
    assert list(module.phases) == [phase, phase2]


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

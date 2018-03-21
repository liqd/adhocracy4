import pytest
from dateutil.parser import parse

from adhocracy4.offlineevents.comparators import cmp_module_offlineevent
from adhocracy4.offlineevents.comparators import cmp_phase_offlineevent


@pytest.mark.django_db
def test_module_comparator(phase_factory, offline_event_factory):
    phase1 = phase_factory(start_date=parse('2013-01-01 00:00:00 UTC'))
    phase2 = phase_factory(start_date=parse('2013-01-02 00:00:00 UTC'))
    phasenone = phase_factory(start_date=None)
    offlineevent1 = offline_event_factory(
        date=parse('2013-01-01 00:00:00 UTC'))
    offlineevent2 = offline_event_factory(
        date=parse('2013-01-02 00:00:00 UTC'))

    assert 0 == cmp_module_offlineevent(phase1.module, phase1.module)
    assert 0 == cmp_module_offlineevent(offlineevent1, offlineevent1)
    assert 0 == cmp_module_offlineevent(phase1.module, offlineevent1)

    assert 1 == cmp_module_offlineevent(phase2.module, phase1.module)
    assert 1 == cmp_module_offlineevent(offlineevent2, offlineevent1)
    assert 1 == cmp_module_offlineevent(phase2.module, offlineevent1)
    assert 1 == cmp_module_offlineevent(offlineevent2, phase1.module)

    assert -1 == cmp_module_offlineevent(phase1.module, phase2.module)
    assert -1 == cmp_module_offlineevent(offlineevent1, offlineevent2)
    assert -1 == cmp_module_offlineevent(phase1.module, offlineevent2)
    assert -1 == cmp_module_offlineevent(offlineevent1, phase2.module)

    assert 1 == cmp_module_offlineevent(phasenone.module, phase1)
    assert 1 == cmp_module_offlineevent(phasenone.module, offlineevent1)
    assert 1 == cmp_module_offlineevent(phasenone.module, phasenone.module)
    assert -1 == cmp_module_offlineevent(phase1.module, phasenone.module)
    assert -1 == cmp_module_offlineevent(offlineevent1, phasenone.module)


@pytest.mark.django_db
def test_phase_comparator(phase_factory, offline_event_factory):
    phase1 = phase_factory(start_date=parse('2013-01-01 00:00:00 UTC'))
    phase2 = phase_factory(start_date=parse('2013-01-02 00:00:00 UTC'))
    phasenone = phase_factory(start_date=None)
    offlineevent1 = offline_event_factory(
        date=parse('2013-01-01 00:00:00 UTC'))
    offlineevent2 = offline_event_factory(
        date=parse('2013-01-02 00:00:00 UTC'))

    assert 0 == cmp_phase_offlineevent(phase1, phase1)
    assert 0 == cmp_phase_offlineevent(offlineevent1, offlineevent1)
    assert 0 == cmp_phase_offlineevent(phase1, offlineevent1)

    assert 1 == cmp_phase_offlineevent(phase2, phase1)
    assert 1 == cmp_phase_offlineevent(offlineevent2, offlineevent1)
    assert 1 == cmp_phase_offlineevent(phase2, offlineevent1)
    assert 1 == cmp_phase_offlineevent(offlineevent2, phase1)

    assert -1 == cmp_phase_offlineevent(phase1, phase2)
    assert -1 == cmp_phase_offlineevent(offlineevent1, offlineevent2)
    assert -1 == cmp_phase_offlineevent(phase1, offlineevent2)
    assert -1 == cmp_phase_offlineevent(offlineevent1, phase2)

    assert 1 == cmp_phase_offlineevent(phasenone, phase1)
    assert 1 == cmp_phase_offlineevent(phasenone, offlineevent1)
    assert 1 == cmp_phase_offlineevent(phasenone, phasenone)
    assert -1 == cmp_phase_offlineevent(phase1, phasenone)
    assert -1 == cmp_phase_offlineevent(offlineevent1, phasenone)

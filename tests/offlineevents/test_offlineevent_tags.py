import pytest

from adhocracy4.offlineevents.templatetags.offlineevent_tags import (
    is_module,
    is_offlineevent,
    is_phase
)


@pytest.mark.django_db
def test_type_templatetags(module, phase, offline_event):
    assert is_phase(phase)
    assert not is_phase(module)
    assert not is_phase(offline_event)

    assert not is_module(phase)
    assert is_module(module)
    assert not is_module(offline_event)

    assert not is_offlineevent(phase)
    assert not is_offlineevent(module)
    assert is_offlineevent(offline_event)

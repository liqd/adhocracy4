import pytest

from adhocracy4.dashboard import components
from meinberlin.apps.activities.dashboard import ActivityComponent

@pytest.mark.django_db
def test_progress(module, activity_factory):
    ac = ActivityComponent()
    assert ac.get_progress(module) == (0, 1)
    activity_factory(module=module)
    assert ac.get_progress(module) == (1, 1)

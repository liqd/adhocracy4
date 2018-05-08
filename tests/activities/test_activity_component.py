import pytest

from adhocracy4.dashboard import components
from meinberlin.apps.activities.dashboard import ActivityComponent

@pytest.mark.django_db
def test_progress(module, activity_factory):
    ac = ActivityComponent()
    assert ac.get_progress(module) == (0, 1)
    activity_factory(module=module)
    assert ac.get_progress(module) == (1, 1)

@pytest.mark.django_db
def test_get_base_url(module, client):
    ac = ActivityComponent()
    url = ac.get_base_url(module)
    resp = client.get(url, follow=True)
    assert resp.status_code != 404  # url exists

@pytest.mark.django_db
def test_call_get_urls(module, client):
    ac = ActivityComponent()
    ac.get_urls()

@pytest.mark.django_db
def test_call_is_effective(module, client):
    ac = ActivityComponent()
    ac.get_urls()

import pytest
from django.core.urlresolvers import reverse

from adhocracy4.test.helpers import redirect_target


@pytest.mark.django_db
def test_detail_view(client, offline_event):
    offline_event_url = reverse('offlineevent-detail',
                                args=[offline_event.slug])

    response = client.get(offline_event_url)
    assert response.status_code == 200
    assert response.context_data['view'].object == offline_event


@pytest.mark.django_db
def test_detail_private_project(client, offline_event_factory, user):
    offline_event = offline_event_factory(project__is_public=False)
    offline_event_url = reverse('offlineevent-detail',
                                args=[offline_event.slug])

    response = client.get(offline_event_url)
    assert response.status_code == 302
    assert redirect_target(response) == 'account_login'

    client.login(username=user, password='password')
    response = client.get(offline_event_url)
    assert response.status_code == 403

    offline_event.project.participants.add(user)
    response = client.get(offline_event_url)
    assert response.status_code == 200
    assert response.context_data['view'].object == offline_event


@pytest.mark.django_db
def test_detail_draft_project(client, offline_event_factory, user, staff_user):
    offline_event = offline_event_factory(project__is_draft=True)
    offline_event_url = reverse('offlineevent-detail',
                                args=[offline_event.slug])

    response = client.get(offline_event_url)
    assert response.status_code == 302
    assert redirect_target(response) == 'account_login'

    client.login(username=user, password='password')
    response = client.get(offline_event_url)
    assert response.status_code == 403

    client.login(username=staff_user, password='password')
    response = client.get(offline_event_url)
    assert response.status_code == 200
    assert response.context_data['view'].object == offline_event

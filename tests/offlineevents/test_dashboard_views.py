import pytest
from dateutil.parser import parse
from django.core.urlresolvers import reverse

from adhocracy4.offlineevents.models import OfflineEvent
from adhocracy4.test.helpers import redirect_target


@pytest.mark.django_db
def test_offlineevent_list(client, project, offline_event_factory,
                           user, staff_user):
    offline_event0 = offline_event_factory(project=project)
    offline_event1 = offline_event_factory(project=project)

    offline_event_list_url = reverse('a4dashboard:offlineevent-list', kwargs={
        'project_slug': project.slug})
    response = client.get(offline_event_list_url)
    assert redirect_target(response) == 'account_login'

    client.login(username=user, password='password')
    response = client.get(offline_event_list_url)
    assert response.status_code == 403

    client.login(username=staff_user, password='password')
    response = client.get(offline_event_list_url)
    assert response.status_code == 200

    object_list = response.context_data['object_list']
    assert list(object_list) == [offline_event0, offline_event1]


@pytest.mark.django_db
def test_offlineevent_create(client, project, user, staff_user):
    offline_event_create_url = reverse('a4dashboard:offlineevent-create',
                                       kwargs={'project_slug': project.slug})

    data = {
        'name': 'offlineevent name',
        'description': 'offlineevent description<script>',
        'date_0': '2013-01-02',
        'date_1': '00:00',
        'form-TOTAL_FORMS': '1',
        'form-INITIAL_FORMS': '0',
        'form-MIN_NUM_FORMS': '0',
        'form-MAX_NUM_FORMS': '5'
    }

    response = client.post(offline_event_create_url, data)
    assert redirect_target(response) == 'account_login'

    client.login(username=user, password='password')
    response = client.post(offline_event_create_url, data)
    assert response.status_code == 403

    client.login(username=staff_user, password='password')
    response = client.post(offline_event_create_url, data)
    assert redirect_target(response) == 'offlineevent-list'

    assert 1 == OfflineEvent.objects.all().count()
    offline_event = OfflineEvent.objects.all().first()
    assert 'offlineevent name' == offline_event.name
    assert 'offlineevent description' == offline_event.description
    assert parse('2013-01-02 00:00:00 UTC') == offline_event.date


@pytest.mark.django_db
def test_offlineevent_update(client, offline_event, user, staff_user):
    offline_event_update_url = reverse('a4dashboard:offlineevent-update',
                                       kwargs={'slug': offline_event.slug})

    data = {
        'name': 'offlineevent name',
        'description': 'offlineevent description<script>',
        'date_0': '2013-01-02',
        'date_1': '00:00',
        'form-TOTAL_FORMS': '1',
        'form-INITIAL_FORMS': '0',
        'form-MIN_NUM_FORMS': '0',
        'form-MAX_NUM_FORMS': '5'
    }

    response = client.post(offline_event_update_url, data)
    assert redirect_target(response) == 'account_login'

    client.login(username=user, password='password')
    response = client.post(offline_event_update_url, data)
    assert response.status_code == 403

    client.login(username=staff_user, password='password')
    response = client.post(offline_event_update_url, data)
    assert redirect_target(response) == 'offlineevent-list'

    assert 1 == OfflineEvent.objects.all().count()
    offline_event = OfflineEvent.objects.all().first()
    assert 'offlineevent name' == offline_event.name
    assert 'offlineevent description' == offline_event.description
    assert parse('2013-01-02 00:00:00 UTC') == offline_event.date


@pytest.mark.django_db
def test_offlineevent_delete(client, offline_event, user, staff_user):
    offline_event_delete_url = reverse('a4dashboard:offlineevent-delete',
                                       kwargs={'slug': offline_event.slug})

    data = {}

    response = client.post(offline_event_delete_url, data)
    assert redirect_target(response) == 'account_login'

    client.login(username=user, password='password')
    response = client.post(offline_event_delete_url, data)
    assert response.status_code == 403

    client.login(username=staff_user, password='password')
    response = client.post(offline_event_delete_url, data)
    assert redirect_target(response) == 'offlineevent-list'

    assert 0 == OfflineEvent.objects.all().count()

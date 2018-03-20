import pytest
from dateutil.parser import parse
from django.core.urlresolvers import reverse

from adhocracy4.dashboard import components
from adhocracy4.test.helpers import redirect_target
from meinberlin.apps.ideas.phases import CollectFeedbackPhase
from meinberlin.apps.offlineevents.models import OfflineEvent
from meinberlin.test.helpers import assert_template_response
from meinberlin.test.helpers import setup_phase

component = components.projects.get('offlineevents')


@pytest.mark.django_db
def test_edit_view(client, phase_factory, offline_event_factory):
    phase, module, project, item = setup_phase(
        phase_factory, None, CollectFeedbackPhase)
    offline_event_factory(project=project)
    initiator = module.project.organisation.initiators.first()
    url = component.get_base_url(project)
    client.login(username=initiator.email, password='password')
    response = client.get(url)
    assert_template_response(
        response, 'meinberlin_offlineevents/offlineevent_list.html')


@pytest.mark.django_db
def test_offlineevent_create_view(client, phase_factory):
    phase, module, project, item = setup_phase(
        phase_factory, None, CollectFeedbackPhase)
    initiator = module.project.organisation.initiators.first()
    url = reverse('a4dashboard:offlineevent-create',
                  kwargs={'project_slug': project.slug})
    data = {
        'name': 'name',
        'description': 'desc',
        'date_0': '2013-01-01',
        'date_1': '18:00',
    }
    client.login(username=initiator.email, password='password')
    response = client.post(url, data)
    assert redirect_target(response) == 'offlineevent-list'
    event = OfflineEvent.objects.get(name=data.get('name'))
    assert event.description == data.get('description')
    assert event.date == parse("2013-01-01 17:00:00 UTC")


@pytest.mark.django_db
def test_offlineevent_update_view(
        client, phase_factory, offline_event_factory):
    phase, module, project, item = setup_phase(
        phase_factory, None, CollectFeedbackPhase)
    initiator = module.project.organisation.initiators.first()
    event = offline_event_factory(project=project)
    url = reverse('a4dashboard:offlineevent-update',
                  kwargs={'slug': event.slug})
    data = {
        'name': 'name',
        'description': 'desc',
        'date_0': '2013-01-01',
        'date_1': '18:00',
    }
    client.login(username=initiator.email, password='password')
    response = client.post(url, data)
    assert redirect_target(response) == 'offlineevent-list'
    event.refresh_from_db()
    assert event.description == data.get('description')
    assert event.date == parse("2013-01-01 17:00:00 UTC")


@pytest.mark.django_db
def test_offlineevent_delete_view(
        client, phase_factory, offline_event_factory):
    phase, module, project, item = setup_phase(
        phase_factory, None, CollectFeedbackPhase)
    initiator = module.project.organisation.initiators.first()
    event = offline_event_factory(project=project)
    url = reverse('a4dashboard:offlineevent-delete',
                  kwargs={'slug': event.slug})
    client.login(username=initiator.email, password='password')
    response = client.delete(url)
    assert redirect_target(response) == 'offlineevent-list'
    assert not OfflineEvent.objects.exists()

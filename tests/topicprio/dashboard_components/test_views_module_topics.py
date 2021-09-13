import pytest
from django.urls import reverse

from adhocracy4.dashboard import components
from adhocracy4.test.helpers import assert_template_response
from adhocracy4.test.helpers import redirect_target
from adhocracy4.test.helpers import setup_phase
from meinberlin.apps.topicprio.models import Topic
from meinberlin.apps.topicprio.phases import PrioritizePhase

component = components.modules.get('topic_edit')


@pytest.mark.django_db
def test_edit_view(client, phase_factory, topic_factory):
    phase, module, project, item = setup_phase(
        phase_factory, topic_factory, PrioritizePhase)
    initiator = module.project.organisation.initiators.first()
    url = component.get_base_url(module)
    client.login(username=initiator.email, password='password')
    response = client.get(url)
    assert_template_response(response,
                             'meinberlin_topicprio/topic_dashboard_list.html')


@pytest.mark.django_db
def test_topic_create_view(client, phase_factory, category_factory):
    phase, module, project, item = setup_phase(
        phase_factory, None, PrioritizePhase)
    initiator = module.project.organisation.initiators.first()
    category = category_factory(module=module)
    url = reverse('a4dashboard:topic-create',
                  kwargs={'module_slug': module.slug})
    data = {
        'name': 'test',
        'description': 'test',
        'category': category.pk
    }
    client.login(username=initiator.email, password='password')
    response = client.post(url, data)
    assert redirect_target(response) == 'topic-list'
    topic = Topic.objects.get(name=data.get('name'))
    assert topic.description == data.get('description')
    assert topic.category.pk == data.get('category')


@pytest.mark.django_db
def test_topic_update_view(
        client, phase_factory, topic_factory, category_factory):
    phase, module, project, item = setup_phase(
        phase_factory, topic_factory, PrioritizePhase)
    initiator = module.project.organisation.initiators.first()
    category = category_factory(module=module)
    url = reverse('a4dashboard:topic-update',
                  kwargs={'pk': item.pk, 'year': item.created.year})
    data = {
        'name': 'test',
        'description': 'test',
        'category': category.pk
    }
    client.login(username=initiator.email, password='password')
    response = client.post(url, data)
    assert redirect_target(response) == 'topic-list'
    item.refresh_from_db()
    assert item.description == data.get('description')
    assert item.category.pk == data.get('category')


@pytest.mark.django_db
def test_topic_delete_view(client, phase_factory, topic_factory):
    phase, module, project, item = setup_phase(
        phase_factory, topic_factory, PrioritizePhase)
    initiator = module.project.organisation.initiators.first()
    url = reverse('a4dashboard:topic-delete',
                  kwargs={'pk': item.pk, 'year': item.created.year})
    client.login(username=initiator.email, password='password')
    response = client.delete(url)
    assert redirect_target(response) == 'topic-list'
    assert not Topic.objects.exists()

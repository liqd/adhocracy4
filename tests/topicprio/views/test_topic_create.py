import pytest
from django.urls import reverse

from adhocracy4.test.helpers import redirect_target
from meinberlin.apps.topicprio import models
from meinberlin.apps.topicprio import phases
from meinberlin.test.helpers import assert_template_response
from meinberlin.test.helpers import freeze_phase
from meinberlin.test.helpers import freeze_pre_phase


@pytest.mark.django_db
def test_anonymous_cannot_create_topic(client, phase_factory):
    phase = phase_factory(phase_content=phases.PrioritizePhase())
    module = phase.module
    url = reverse('a4dashboard:topic-create',
                  kwargs={'module_slug': module.slug})
    with freeze_phase(phase):
        count = models.Topic.objects.all().count()
        assert count == 0
        response = client.get(url)
        assert response.status_code == 302
        assert redirect_target(response) == 'account_login'


@pytest.mark.django_db
def test_user_cannot_create_topic(client, phase_factory, user):
    phase = phase_factory(phase_content=phases.PrioritizePhase())
    module = phase.module
    url = reverse('a4dashboard:topic-create',
                  kwargs={'module_slug': module.slug})
    with freeze_phase(phase):
        response = client.get(url)
        assert response.status_code == 302
        client.login(username=user.email, password='password')
        response = client.get(url)
        assert response.status_code == 403


@pytest.mark.django_db
def test_admin_can_create_topic(client, phase_factory,
                                category_factory, admin):
    phase = phase_factory(phase_content=phases.PrioritizePhase())
    module = phase.module
    category = category_factory(module=module)
    url = reverse('a4dashboard:topic-create',
                  kwargs={'module_slug': module.slug})
    with freeze_phase(phase):
        client.login(username=admin.email, password='password')
        response = client.get(url)
        assert_template_response(
            response, 'meinberlin_topicprio/topic_create_form.html')
        assert response.status_code == 200
        topic = {
            'name': 'Topic',
            'description': 'description',
            'category': category.pk,
        }
        response = client.post(url, topic)
        assert response.status_code == 302
        assert redirect_target(response) == 'topic-list'
        count = models.Topic.objects.all().count()
        assert count == 1


@pytest.mark.django_db
def test_moderator_can_create_topic_before_phase(client, phase_factory,
                                                 category_factory, admin):
    phase = phase_factory(phase_content=phases.PrioritizePhase())
    module = phase.module
    project = module.project
    category = category_factory(module=module)
    moderator = project.moderators.first()
    url = reverse('a4dashboard:topic-create',
                  kwargs={'module_slug': module.slug})
    with freeze_pre_phase(phase):
        client.login(username=moderator.email, password='password')
        response = client.get(url)
        assert_template_response(
            response, 'meinberlin_topicprio/topic_create_form.html')
        assert response.status_code == 200
        topic = {
            'name': 'Topic',
            'description': 'description',
            'category': category.pk,
        }
        response = client.post(url, topic)
        assert response.status_code == 302
        assert redirect_target(response) == 'topic-list'
        count = models.Topic.objects.all().count()
        assert count == 1


@pytest.mark.django_db
def test_initiator_can_create_topic_before_phase(client, phase_factory,
                                                 category_factory, admin):
    phase = phase_factory(phase_content=phases.PrioritizePhase())
    module = phase.module
    project = module.project
    category = category_factory(module=module)
    initiator = project.organisation.initiators.first()
    url = reverse('a4dashboard:topic-create',
                  kwargs={'module_slug': module.slug})
    with freeze_pre_phase(phase):
        client.login(username=initiator.email, password='password')
        response = client.get(url)
        assert_template_response(
            response, 'meinberlin_topicprio/topic_create_form.html')
        assert response.status_code == 200
        topic = {
            'name': 'Topic',
            'description': 'description',
            'category': category.pk,
        }
        response = client.post(url, topic)
        assert response.status_code == 302
        assert redirect_target(response) == 'topic-list'
        count = models.Topic.objects.all().count()
        assert count == 1

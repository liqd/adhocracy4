from unittest.mock import ANY
from unittest.mock import MagicMock

import pytest
from django.urls import reverse

from adhocracy4.dashboard import components
from adhocracy4.dashboard.signals import module_component_updated
from adhocracy4.test.helpers import assert_template_response
from adhocracy4.test.helpers import freeze_phase
from adhocracy4.test.helpers import freeze_pre_phase
from adhocracy4.test.helpers import redirect_target
from meinberlin.apps.topicprio import models
from meinberlin.apps.topicprio import phases

component = components.modules.get("topic_edit")


@pytest.mark.django_db
def test_anonymous_cannot_create_topic(client, phase_factory):
    phase = phase_factory(phase_content=phases.PrioritizePhase())
    module = phase.module
    url = reverse("a4dashboard:topic-create", kwargs={"module_slug": module.slug})
    with freeze_phase(phase):
        count = models.Topic.objects.all().count()
        assert count == 0
        response = client.get(url)
        assert response.status_code == 302
        assert redirect_target(response) == "account_login"


@pytest.mark.django_db
def test_user_cannot_create_topic(client, phase_factory, user):
    phase = phase_factory(phase_content=phases.PrioritizePhase())
    module = phase.module
    url = reverse("a4dashboard:topic-create", kwargs={"module_slug": module.slug})
    with freeze_phase(phase):
        response = client.get(url)
        assert response.status_code == 302
        client.login(username=user.email, password="password")
        response = client.get(url)
        assert response.status_code == 403


@pytest.mark.django_db
def test_admin_can_create_topic(client, phase_factory, category_factory, admin):
    phase = phase_factory(phase_content=phases.PrioritizePhase())
    module = phase.module
    category = category_factory(module=module)
    url = reverse("a4dashboard:topic-create", kwargs={"module_slug": module.slug})
    with freeze_phase(phase):
        client.login(username=admin.email, password="password")
        response = client.get(url)
        assert_template_response(
            response, "meinberlin_topicprio/topic_create_form.html"
        )
        topic = {
            "name": "Topic",
            "description": "description",
            "category": category.pk,
        }
        signal_handler = MagicMock()
        module_component_updated.connect(signal_handler)
        response = client.post(url, topic)
        signal_handler.assert_called_once_with(
            signal=ANY,
            sender=component.__class__,
            module=module,
            component=component,
            user=admin,
        )
        assert response.status_code == 302
        assert redirect_target(response) == "topic-list"
        count = models.Topic.objects.all().count()
        assert count == 1


@pytest.mark.django_db
def test_moderator_cannot_create_topic_before_phase(
    client, phase_factory, category_factory, admin
):
    phase = phase_factory(phase_content=phases.PrioritizePhase())
    module = phase.module
    project = module.project
    moderator = project.moderators.first()
    url = reverse("a4dashboard:topic-create", kwargs={"module_slug": module.slug})
    with freeze_pre_phase(phase):
        client.login(username=moderator.email, password="password")
        response = client.get(url)
        assert response.status_code == 403


@pytest.mark.django_db
def test_initiator_can_create_topic_before_phase(
    client, phase_factory, category_factory, admin
):
    phase = phase_factory(phase_content=phases.PrioritizePhase())
    module = phase.module
    project = module.project
    category = category_factory(module=module)
    initiator = project.organisation.initiators.first()
    url = reverse("a4dashboard:topic-create", kwargs={"module_slug": module.slug})
    with freeze_pre_phase(phase):
        client.login(username=initiator.email, password="password")
        response = client.get(url)
        assert_template_response(
            response, "meinberlin_topicprio/topic_create_form.html"
        )
        topic = {
            "name": "Topic",
            "description": "description",
            "category": category.pk,
        }
        signal_handler = MagicMock()
        module_component_updated.connect(signal_handler)
        response = client.post(url, topic)
        signal_handler.assert_called_once_with(
            signal=ANY,
            sender=component.__class__,
            module=module,
            component=component,
            user=initiator,
        )
        assert response.status_code == 302
        assert redirect_target(response) == "topic-list"
        count = models.Topic.objects.all().count()
        assert count == 1

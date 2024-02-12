from unittest.mock import ANY
from unittest.mock import MagicMock

import pytest
from django.urls import reverse

from adhocracy4.dashboard import components
from adhocracy4.dashboard.signals import module_component_updated
from adhocracy4.test.helpers import redirect_target
from meinberlin.apps.topicprio import models

component = components.modules.get("topic_edit")


@pytest.mark.django_db
def test_anonymous_cannot_delete(client, topic_factory):
    topic = topic_factory()
    url = reverse(
        "a4dashboard:topic-delete", kwargs={"pk": topic.pk, "year": topic.created.year}
    )
    signal_handler = MagicMock()
    module_component_updated.connect(signal_handler)
    response = client.post(url)
    assert response.status_code == 302
    assert redirect_target(response) == "account_login"
    signal_handler.assert_not_called()


@pytest.mark.django_db
def test_user_cannot_delete(client, topic_factory, user):
    topic = topic_factory()
    client.login(username=user.email, password="password")
    url = reverse(
        "a4dashboard:topic-delete", kwargs={"pk": topic.pk, "year": topic.created.year}
    )
    response = client.post(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_moderator_cannot_delete(client, topic_factory):
    topic = topic_factory()
    moderator = topic.module.project.moderators.first()
    client.login(username=moderator.email, password="password")
    url = reverse(
        "a4dashboard:topic-delete", kwargs={"pk": topic.pk, "year": topic.created.year}
    )
    response = client.post(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_initator_can_delete(client, topic_factory):
    topic = topic_factory()
    initiator = topic.module.project.organisation.initiators.first()
    client.login(username=initiator.email, password="password")
    url = reverse(
        "a4dashboard:topic-delete", kwargs={"pk": topic.pk, "year": topic.created.year}
    )
    signal_handler = MagicMock()
    module_component_updated.connect(signal_handler)
    response = client.post(url)
    assert response.status_code == 302
    assert redirect_target(response) == "topic-list"
    count = models.Topic.objects.all().count()
    assert count == 0
    signal_handler.assert_called_once_with(
        signal=ANY,
        sender=component.__class__,
        module=topic.module,
        component=component,
        user=initiator,
    )


@pytest.mark.django_db
def test_admin_can_delete(client, topic_factory, admin):
    topic = topic_factory()
    client.login(username=admin.email, password="password")
    url = reverse(
        "a4dashboard:topic-delete", kwargs={"pk": topic.pk, "year": topic.created.year}
    )
    signal_handler = MagicMock()
    module_component_updated.connect(signal_handler)
    response = client.post(url)
    assert response.status_code == 302
    assert redirect_target(response) == "topic-list"
    count = models.Topic.objects.all().count()
    assert count == 0
    signal_handler.assert_called_once_with(
        signal=ANY,
        sender=component.__class__,
        module=topic.module,
        component=component,
        user=admin,
    )

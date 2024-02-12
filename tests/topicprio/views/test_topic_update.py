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
def test_user_cannot_update(client, topic_factory):
    topic = topic_factory()
    user = topic.creator
    assert user not in topic.module.project.moderators.all()
    url = reverse(
        "a4dashboard:topic-update", kwargs={"pk": topic.pk, "year": topic.created.year}
    )
    client.login(username=user.email, password="password")
    data = {"name": "Another Topic", "description": "changed description"}
    signal_handler = MagicMock()
    module_component_updated.connect(signal_handler)
    response = client.post(url, data)
    assert response.status_code == 403
    signal_handler.assert_not_called()


@pytest.mark.django_db
def test_moderators_cannot_update(client, topic_factory):
    topic = topic_factory()
    moderator = topic.module.project.moderators.first()
    assert moderator is not topic.creator
    url = reverse(
        "a4dashboard:topic-update", kwargs={"pk": topic.pk, "year": topic.created.year}
    )
    client.login(username=moderator.email, password="password")
    data = {"name": "Another Topic", "description": "changed description"}
    signal_handler = MagicMock()
    module_component_updated.connect(signal_handler)
    response = client.post(url, data)
    assert response.status_code == 403
    signal_handler.assert_not_called()


@pytest.mark.django_db
def test_initiators_can_always_update(client, topic_factory):
    topic = topic_factory()
    initiator = topic.module.project.organisation.initiators.first()
    assert initiator is not topic.creator
    url = reverse(
        "a4dashboard:topic-update", kwargs={"pk": topic.pk, "year": topic.created.year}
    )
    client.login(username=initiator.email, password="password")
    data = {"name": "Another Topic", "description": "changed description"}
    signal_handler = MagicMock()
    module_component_updated.connect(signal_handler)
    response = client.post(url, data)
    assert redirect_target(response) == "topic-list"
    assert response.status_code == 302
    updated_topic = models.Topic.objects.get(id=topic.pk)
    assert updated_topic.description == "changed description"
    signal_handler.assert_called_once_with(
        signal=ANY,
        sender=component.__class__,
        module=topic.module,
        component=component,
        user=initiator,
    )

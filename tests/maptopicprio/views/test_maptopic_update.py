import pytest
from django.urls import reverse

from adhocracy4.test.helpers import redirect_target
from meinberlin.apps.maptopicprio import models


@pytest.mark.django_db
def test_user_cannot_update(client, user, maptopic_factory, area_settings_factory):
    maptopic = maptopic_factory()
    area_settings_factory(module=maptopic.module)
    assert user not in maptopic.module.project.moderators.all()
    url = reverse(
        "a4dashboard:maptopic-update",
        kwargs={"pk": maptopic.pk, "year": maptopic.created.year},
    )
    client.login(username=user.email, password="password")
    data = {
        "name": "Another MapTopic",
        "description": "changed description",
        "point": (0, 0),
        "point_label": "somewhere",
    }
    response = client.post(url, data)
    assert response.status_code == 403


@pytest.mark.django_db
def test_moderators_cannot_update(client, maptopic_factory, area_settings_factory):
    maptopic = maptopic_factory()
    moderator = maptopic.module.project.moderators.first()
    area_settings_factory(module=maptopic.module)
    assert moderator is not maptopic.creator
    url = reverse(
        "a4dashboard:maptopic-update",
        kwargs={"pk": maptopic.pk, "year": maptopic.created.year},
    )
    client.login(username=moderator.email, password="password")
    data = {
        "name": "Another MapTopic",
        "description": "changed description",
        "point": (0, 0),
        "point_label": "somewhere",
    }
    response = client.post(url, data)
    assert response.status_code == 403


@pytest.mark.django_db
def test_initiators_can_always_update(client, maptopic_factory, area_settings_factory):
    maptopic = maptopic_factory()
    initiator = maptopic.module.project.organisation.initiators.first()
    area_settings_factory(module=maptopic.module)
    assert initiator is not maptopic.creator
    url = reverse(
        "a4dashboard:maptopic-update",
        kwargs={"pk": maptopic.pk, "year": maptopic.created.year},
    )
    client.login(username=initiator.email, password="password")
    data = {
        "name": "Another MapTopic",
        "description": "changed description",
        "point": (0, 0),
        "point_label": "somewhere",
    }
    response = client.post(url, data)
    assert redirect_target(response) == "maptopic-list"
    assert response.status_code == 302
    updated_maptopic = models.MapTopic.objects.get(id=maptopic.pk)
    assert updated_maptopic.description == "changed description"

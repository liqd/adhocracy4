import pytest
from django.urls import reverse

from adhocracy4.test.helpers import redirect_target
from meinberlin.apps.maptopicprio import models


@pytest.mark.django_db
def test_anonymous_cannot_delete(client, maptopic_factory):
    maptopic = maptopic_factory()
    url = reverse(
        'a4dashboard:maptopic-delete',
        kwargs={
            'pk': maptopic.pk,
            'year': maptopic.created.year
        })
    response = client.post(url)
    assert response.status_code == 302
    assert redirect_target(response) == 'account_login'


@pytest.mark.django_db
def test_user_cannot_delete(client, maptopic_factory, user):
    maptopic = maptopic_factory()
    client.login(username=user.email, password='password')
    url = reverse(
        'a4dashboard:maptopic-delete',
        kwargs={
            'pk': maptopic.pk,
            'year': maptopic.created.year
        })
    response = client.post(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_moderator_cannot_delete(client, maptopic_factory):
    maptopic = maptopic_factory()
    moderator = maptopic.module.project.moderators.first()
    client.login(username=moderator.email, password='password')
    url = reverse(
        'a4dashboard:maptopic-delete',
        kwargs={
            'pk': maptopic.pk,
            'year': maptopic.created.year
        })
    response = client.post(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_initator_can_delete(client, maptopic_factory):
    maptopic = maptopic_factory()
    initiator = maptopic.module.project.organisation.initiators.first()
    client.login(username=initiator.email, password='password')
    url = reverse(
        'a4dashboard:maptopic-delete',
        kwargs={
            'pk': maptopic.pk,
            'year': maptopic.created.year
        })
    response = client.post(url)
    assert response.status_code == 302
    assert redirect_target(response) == 'maptopic-list'
    count = models.MapTopic.objects.all().count()
    assert count == 0


@pytest.mark.django_db
def test_admin_can_delete(client, maptopic_factory, admin):
    maptopic = maptopic_factory()
    client.login(username=admin.email, password='password')
    url = reverse(
        'a4dashboard:maptopic-delete',
        kwargs={
            'pk': maptopic.pk,
            'year': maptopic.created.year
        })
    response = client.post(url)
    assert response.status_code == 302
    assert redirect_target(response) == 'maptopic-list'
    count = models.MapTopic.objects.all().count()
    assert count == 0

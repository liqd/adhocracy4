import pytest
from django.urls import reverse

from adhocracy4.test.helpers import redirect_target
from meinberlin.apps.topicprio import models


@pytest.mark.django_db
def test_anonymous_cannot_delete(client, topic_factory):
    topic = topic_factory()
    url = reverse(
        'a4dashboard:topic-delete',
        kwargs={
            'pk': topic.pk,
            'year': topic.created.year
        })
    response = client.post(url)
    assert response.status_code == 302
    assert redirect_target(response) == 'account_login'


@pytest.mark.django_db
def test_user_cannot_delete(client, topic_factory, user):
    topic = topic_factory()
    client.login(username=user.email, password='password')
    url = reverse(
        'a4dashboard:topic-delete',
        kwargs={
            'pk': topic.pk,
            'year': topic.created.year
        })
    response = client.post(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_moderator_cannot_delete(client, topic_factory):
    topic = topic_factory()
    moderator = topic.module.project.moderators.first()
    client.login(username=moderator.email, password='password')
    url = reverse(
        'a4dashboard:topic-delete',
        kwargs={
            'pk': topic.pk,
            'year': topic.created.year
        })
    response = client.post(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_initator_can_delete(client, topic_factory):
    topic = topic_factory()
    initiator = topic.module.project.organisation.initiators.first()
    client.login(username=initiator.email, password='password')
    url = reverse(
        'a4dashboard:topic-delete',
        kwargs={
            'pk': topic.pk,
            'year': topic.created.year
        })
    response = client.post(url)
    assert response.status_code == 302
    assert redirect_target(response) == 'topic-list'
    count = models.Topic.objects.all().count()
    assert count == 0


@pytest.mark.django_db
def test_admin_can_delete(client, topic_factory, admin):
    topic = topic_factory()
    client.login(username=admin.email, password='password')
    url = reverse(
        'a4dashboard:topic-delete',
        kwargs={
            'pk': topic.pk,
            'year': topic.created.year
        })
    response = client.post(url)
    assert response.status_code == 302
    assert redirect_target(response) == 'topic-list'
    count = models.Topic.objects.all().count()
    assert count == 0

import pytest
from django.urls import reverse
from rest_framework import status

from adhocracy4.follows import models as follow_models


@pytest.mark.django_db
def test_anonymous_user_has_no_follow(apiclient):
    url = reverse('follows-list')
    response = apiclient.get(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_user_list_follows(apiclient, follow):
    url = reverse('follows-list')
    apiclient.force_authenticate(user=follow.creator)
    response = apiclient.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data[0]['project'] == follow.project.slug
    assert response.data[0]['enabled'] is True


@pytest.mark.django_db
def test_user_add_follow(apiclient, project, user):
    url = reverse('follows-detail', args=[project.slug])
    apiclient.force_authenticate(user=user)
    response = apiclient.put(url)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['project'] == project.slug
    follow = follow_models.Follow.objects.get(creator=user, project=project)
    assert follow.enabled is True

    response = apiclient.put(url, {'enabled': False}, format='json')
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_user_unfollow(apiclient, follow):
    project = follow.project
    user = follow.creator
    url = reverse('follows-detail', kwargs={'project__slug': project.slug})
    apiclient.force_authenticate(user=user)
    response = apiclient.put(url, {'enabled': False}, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['project'] == project.slug
    follow = follow_models.Follow.objects.get(creator=user, project=project)
    assert follow.enabled is False

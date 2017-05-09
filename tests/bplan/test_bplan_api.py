import pytest
from django.core.urlresolvers import reverse
from rest_framework import status

from apps.bplan import models as bplan_models


@pytest.mark.django_db
def test_anonymous_cannot_add_bplan(apiclient, organisation):
    url = reverse('bplan-list', kwargs={'organisation_pk': organisation.pk})
    data = {}
    response = apiclient.post(url, data, format='json')
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_non_initiator_cannot_add_bplan(apiclient, organisation, user):
    url = reverse('bplan-list', kwargs={'organisation_pk': organisation.pk})
    data = {}
    apiclient.force_authenticate(user=user)
    response = apiclient.post(url, data, format='json')
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_initiator_add_bplan(apiclient, organisation):
    url = reverse('bplan-list', kwargs={'organisation_pk': organisation.pk})
    data = {
        "name": "bplan-1",
        "description": "desc",
        "url": "https://bplan.net",
        "office_worker_email": "test@liqd.de",
        "is_archived": "false",
    }
    user = organisation.initiators.first()
    apiclient.force_authenticate(user=user)
    response = apiclient.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    bplan = bplan_models.Bplan.objects.first()
    assert bplan.name == data['name']
    assert bplan.description == data['description']
    assert bplan.url == data['url']
    assert bplan.office_worker_email == data['office_worker_email']
    assert bplan.is_archived is False
    assert bplan.is_draft is False
    assert bplan.information == ''
    assert bplan.result == ''


@pytest.mark.django_db
def test_initiator_update_bplan(apiclient, bplan):
    url = reverse(
        'bplan-detail',
        kwargs={
            'organisation_pk': bplan.organisation.pk,
            'pk': bplan.pk
        }
    )
    data = {
        "name": "bplan-1",
        "description": "desc",
        "url": "https://bplan.net",
        "office_worker_email": "test@liqd.de",
        "is_archived": "true",
    }
    user = bplan.organisation.initiators.first()
    apiclient.force_authenticate(user=user)
    response = apiclient.put(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    bplan = bplan_models.Bplan.objects.first()
    assert bplan.is_archived is True


@pytest.mark.django_db
def test_non_initiator_cannot_update_bplan(apiclient, bplan, user2):
    url = reverse(
        'bplan-detail',
        kwargs={
            'organisation_pk': bplan.organisation.pk,
            'pk': bplan.pk
        }
    )
    data = {}
    apiclient.force_authenticate(user=user2)
    response = apiclient.put(url, data, format='json')
    assert response.status_code == status.HTTP_403_FORBIDDEN

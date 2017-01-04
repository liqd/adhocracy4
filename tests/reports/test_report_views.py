import pytest
from django.core.urlresolvers import reverse
from rest_framework import status


@pytest.mark.django_db
def test_anonymous_user_can_not_report(apiclient):
    url = reverse('reports-list')
    data = {}
    response = apiclient.post(url, data, format='json')
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_anonymous_user_can_not_view_reportlist(apiclient):
    url = reverse('reports-list')
    response = apiclient.get(url, format='json')
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_authenticated_user_can_not_report_invalid_data(apiclient, user):
    apiclient.force_authenticate(user=user)
    url = reverse('reports-list')
    data = {}
    response = apiclient.post(url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_authenticated_user_can_not_view_reportlist(apiclient, user):
    apiclient.force_authenticate(user=user)
    url = reverse('reports-list')
    response = apiclient.get(url, format='json')
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

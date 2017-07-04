import pytest
from django.contrib.contenttypes.models import ContentType
from django.core import mail
from django.core.urlresolvers import reverse
from rest_framework import status

from adhocracy4.test.helpers import skip_background_mail


@pytest.mark.django_db
def test_anonymous_user_can_not_get_report_list(apiclient):
    url = reverse('reports-list')
    response = apiclient.get(url, format='json')
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_authenticated_user_can_not_get_report_list(apiclient, user):
    url = reverse('reports-list')
    apiclient.force_authenticate(user=user)
    response = apiclient.get(url, format='json')
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.django_db
def test_anonymous_user_can_not_report(apiclient):
    url = reverse('reports-list')
    data = {}
    response = apiclient.post(url, data, format='json')
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_authenticated_user_can_not_post_invalid_data(user,
                                                      apiclient):
    apiclient.force_authenticate(user=user)
    url = reverse('reports-list')
    data = {}
    response = apiclient.post(url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_authenticated_user_can_post_valid_data(user,
                                                apiclient,
                                                question,
                                                admin):
    apiclient.force_authenticate(user=user)
    url = reverse('reports-list')
    question_ct = ContentType.objects.get_for_model(question)
    data = {
        'content_type': question_ct.pk,
        'object_pk': question.pk,
        'description': 'This comment sucks'
    }
    with skip_background_mail():
        response = apiclient.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['description'] == 'This comment sucks'
    assert len(mail.outbox) == 2
    assert mail.outbox[0].subject.startswith('Moderation request in')
    assert mail.outbox[1].subject.startswith('Your question was reported')

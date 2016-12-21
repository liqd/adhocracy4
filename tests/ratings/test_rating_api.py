import pytest
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from rest_framework import status


@pytest.mark.django_db
def test_anonymous_user_can_not_get_rating_list(apiclient):
    url = reverse('ratings-list')
    response = apiclient.get(url, format='json')
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.django_db
def test_authenticated_user_can_not_get_rating_list(apiclient, user):
    url = reverse('ratings-list')
    apiclient.force_authenticate(user=user)
    response = apiclient.get(url, format='json')
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.django_db
def test_anonymous_user_can_not_rating(apiclient):
    url = reverse('ratings-list')
    data = {}
    response = apiclient.post(url, data, format='json')
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_authenticated_user_can_not_post_invalid_data(user, apiclient):
    apiclient.force_authenticate(user=user)
    url = reverse('ratings-list')
    data = {}
    response = apiclient.post(url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_authenticated_user_can_post_valid_data(user, apiclient):
    apiclient.force_authenticate(user=user)
    url = reverse('ratings-list')
    data = {
        'value': 1,
        'object_pk': 1,
        'content_type': 1
    }
    response = apiclient.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_authenticated_user_can_edit_own_rating(rating_factory,
                                                question,
                                                apiclient):
    ct = ContentType.objects.get_for_model(question)
    rating = rating_factory(object_pk=question.id, content_type=ct)
    apiclient.force_authenticate(user=rating.creator)
    data = {'value': 1}
    url = reverse('ratings-detail', kwargs={'pk': rating.pk})
    response = apiclient.patch(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['value'] == 1


@pytest.mark.django_db
def test_authenticated_user_can_rating_higher_1(rating_factory,
                                                question,
                                                apiclient):
    ct = ContentType.objects.get_for_model(question)
    rating = rating_factory(object_pk=question.id, content_type=ct)
    apiclient.force_authenticate(user=rating.creator)
    data = {'value': 10}
    url = reverse('ratings-detail', kwargs={'pk': rating.pk})
    response = apiclient.patch(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['value'] == 1


@pytest.mark.django_db
def test_authenticated_user_can_rating_lower_minus1(rating_factory,
                                                    question,
                                                    apiclient):
    ct = ContentType.objects.get_for_model(question)
    rating = rating_factory(object_pk=question.id, content_type=ct)
    apiclient.force_authenticate(user=rating.creator)
    data = {'value': -10}
    url = reverse('ratings-detail', kwargs={'pk': rating.pk})
    response = apiclient.patch(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['value'] == -1


@pytest.mark.django_db
def test_anonymous_user_can_not_delete_rating(rating, apiclient):
    apiclient.force_authenticate(user=None)
    url = reverse('ratings-detail', kwargs={'pk': rating.pk})
    response = apiclient.delete(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_authenticated_user_can_not_delete_rating(rating, another_user, apiclient):
    url = reverse('ratings-detail', kwargs={'pk': rating.pk})
    apiclient.force_authenticate(user=another_user)
    response = apiclient.delete(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_creater_of_rating_can_set_zero(rating_factory, question,  apiclient):
    ct = ContentType.objects.get_for_model(question)
    rating = rating_factory(object_pk=question.id, content_type=ct)
    url = reverse('ratings-detail', kwargs={'pk': rating.pk})
    apiclient.force_authenticate(user=rating.creator)
    response = apiclient.delete(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['value'] == 0


@pytest.mark.django_db
def test_meta_info_of_rating(rating_factory, question,  apiclient, user, another_user):
    ct = ContentType.objects.get_for_model(question)
    pk = question.pk
    url = reverse('ratings-list')
    apiclient.force_authenticate(user)
    data = {
        'value': 1,
        'object_pk': pk,
        'content_type': ct.pk
    }
    response = apiclient.post(url, data, format='json')
    rating_id = response.data['id']
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['value'] == 1
    metadata = response.data['meta_info']
    assert metadata['positive_ratings_on_same_object'] == 1
    assert metadata['user_rating_on_same_object_value'] == 1
    assert metadata['user_rating_on_same_object_id'] == rating_id
    apiclient.force_authenticate(another_user)
    response = apiclient.post(url, data, format='json')
    rating_id = response.data['id']
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['value'] == 1
    metadata = response.data['meta_info']
    assert metadata['positive_ratings_on_same_object'] == 2
    assert metadata['user_rating_on_same_object_value'] == 1
    assert metadata['user_rating_on_same_object_id'] == rating_id

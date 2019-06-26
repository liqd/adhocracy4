import pytest
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from rest_framework import status

from tests.apps.questions.models import Question
from tests.apps.questions.phases import RatePhase
from tests.helpers import active_phase


@pytest.mark.django_db
@pytest.fixture
def question_ct():
    return ContentType.objects.get_for_model(Question)


@pytest.mark.django_db
def test_anonymous_user_rating_list(apiclient, question, question_ct):
    url = reverse(
        'ratings-list',
        kwargs={'content_type': question_ct.pk,
                'object_pk': question.pk})
    response = apiclient.get(url, format='json')
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_authenticated_user_rating_list(apiclient, user, question,
                                        question_ct):
    url = reverse(
        'ratings-list',
        kwargs={'content_type': question_ct.pk,
                'object_pk': question.pk})
    apiclient.force_authenticate(user=user)
    response = apiclient.get(url, format='json')
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_anonymous_user_can_not_rating(apiclient, question, question_ct):
    url = reverse(
        'ratings-list',
        kwargs={'content_type': question_ct.pk,
                'object_pk': question.pk})
    data = {}

    with active_phase(question.module, RatePhase):
        response = apiclient.post(url, data, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_post_invalid_data(user, apiclient, question, question_ct):
    apiclient.force_authenticate(user=user)
    url = reverse(
        'ratings-list',
        kwargs={'content_type': question_ct.pk,
                'object_pk': question.pk})
    data = {}

    with active_phase(question.module, RatePhase):
        response = apiclient.post(url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_post_valid_data(user, apiclient, question, question_ct):
    apiclient.force_authenticate(user=user)
    url = reverse(
        'ratings-list',
        kwargs={'content_type': question_ct.pk,
                'object_pk': question.pk})
    data = {
        'value': 1,
    }

    with active_phase(question.module, RatePhase):
        response = apiclient.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_authenticated_user_can_edit_own_rating(rating, question_ct,
                                                apiclient):
    question = rating.content_object
    apiclient.force_authenticate(user=rating.creator)
    data = {'value': 0}
    url = reverse(
        'ratings-detail',
        kwargs={
            'pk': rating.pk,
            'content_type': question_ct.pk,
            'object_pk': question.pk
        })

    with active_phase(question.module, RatePhase):
        response = apiclient.patch(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['value'] == 0


@pytest.mark.django_db
def test_authenticated_user_can_rating_higher_1(rating, question,
                                                question_ct, apiclient):
    question = rating.content_object
    apiclient.force_authenticate(user=rating.creator)
    data = {'value': 10}
    url = reverse(
        'ratings-detail',
        kwargs={
            'pk': rating.pk,
            'content_type': question_ct.pk,
            'object_pk': question.pk
        })

    with active_phase(question.module, RatePhase):
        response = apiclient.patch(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['value'] == 1


@pytest.mark.django_db
def test_authenticated_user_can_rating_lower_minus1(rating, question,
                                                    question_ct, apiclient):
    question = rating.content_object
    apiclient.force_authenticate(user=rating.creator)
    data = {'value': -10}
    url = reverse(
        'ratings-detail',
        kwargs={
            'pk': rating.pk,
            'content_type': question_ct.pk,
            'object_pk': question.pk
        })

    with active_phase(question.module, RatePhase):
        response = apiclient.patch(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['value'] == -1


@pytest.mark.django_db
def test_anonymous_user_can_not_delete_rating(rating, apiclient):
    apiclient.force_authenticate(user=None)
    url = reverse(
        'ratings-detail',
        kwargs={
            'pk': rating.pk,
            'content_type': rating.content_type.pk,
            'object_pk': rating.object_pk
        })

    with active_phase(rating.content_object.module, RatePhase):
        response = apiclient.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_authenticated_user_can_not_delete_rating(rating, another_user,
                                                  apiclient):
    url = reverse(
        'ratings-detail',
        kwargs={
            'pk': rating.pk,
            'content_type': rating.content_type.pk,
            'object_pk': rating.object_pk
        })
    apiclient.force_authenticate(user=another_user)

    with active_phase(rating.content_object.module, RatePhase):
        response = apiclient.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_creator_of_rating_can_set_zero(rating, question_ct, apiclient):
    question = rating.content_object
    url = reverse(
        'ratings-detail',
        kwargs={
            'pk': rating.pk,
            'content_type': rating.content_type.pk,
            'object_pk': rating.object_pk,
        })
    apiclient.force_authenticate(user=rating.creator)

    with active_phase(question.module, RatePhase):
        response = apiclient.delete(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['value'] == 0


@pytest.mark.django_db
def test_meta_info_of_rating(rating_factory, question, question_ct, apiclient,
                             user, another_user):
    apiclient.force_authenticate(user)
    url = reverse(
        'ratings-list',
        kwargs={'content_type': question_ct.pk,
                'object_pk': question.pk})
    data = {'value': 1}

    with active_phase(question.module, RatePhase):
        response = apiclient.post(url, data, format='json')
        rating_id = response.data['id']
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['value'] == 1
        metadata = response.data['meta_info']
        assert metadata['positive_ratings_on_same_object'] == 1
        assert metadata['user_rating_on_same_object_value'] == 1
        assert metadata['user_rating_on_same_object_id'] == rating_id

    apiclient.force_authenticate(another_user)

    with active_phase(question.module, RatePhase):
        response = apiclient.post(url, data, format='json')
        rating_id = response.data['id']
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['value'] == 1
        metadata = response.data['meta_info']
        assert metadata['positive_ratings_on_same_object'] == 2
        assert metadata['user_rating_on_same_object_value'] == 1
        assert metadata['user_rating_on_same_object_id'] == rating_id

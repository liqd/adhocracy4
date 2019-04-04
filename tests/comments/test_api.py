import pytest
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from rest_framework import status

from tests.apps.questions.models import Question
from tests.apps.questions.phases import AskPhase
from tests.helpers import active_phase


@pytest.mark.django_db
@pytest.fixture
def question_ct():
    return ContentType.objects.get_for_model(Question)


@pytest.mark.django_db
def test_anonymous_user_can_not_comment(apiclient, question_ct, question):
    url = reverse(
        'comments-list',
        kwargs={'content_type': question_ct.pk,
                'object_pk': question.pk})
    data = {
        'comment': 'no comment',
    }
    response = apiclient.post(url, data, format='json')
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_authenticated_user_can_not_post_invalid_data(user, apiclient,
                                                      question_ct, question):
    apiclient.force_authenticate(user=user)
    url = reverse(
        'comments-list',
        kwargs={'content_type': question_ct.pk,
                'object_pk': question.pk})
    data = {}

    with active_phase(question.module, AskPhase):
        response = apiclient.post(url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_authenticated_user_can_post_valid_data(user, question_ct, question,
                                                apiclient):
    apiclient.force_authenticate(user=user)
    url = reverse(
        'comments-list',
        kwargs={'content_type': question_ct.pk,
                'object_pk': question.pk})
    data = {'comment': 'comment comment'}

    with active_phase(question.module, AskPhase):
        response = apiclient.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_authenticated_user_can_edit_own_comment(comment, apiclient):
    apiclient.force_authenticate(user=comment.creator)
    url = reverse(
        'comments-detail',
        kwargs={
            'pk': comment.pk,
            'content_type': comment.content_type.pk,
            'object_pk': comment.object_pk
        })
    data = {'comment': 'comment comment comment'}

    with active_phase(comment.content_object.module, AskPhase):
        response = apiclient.patch(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['comment'] == 'comment comment comment'


@pytest.mark.django_db
def test_user_can_not_edit_comment_of_other_user(another_user, comment,
                                                 apiclient):
    apiclient.force_authenticate(user=another_user)
    url = reverse(
        'comments-detail',
        kwargs={
            'pk': comment.pk,
            'content_type': comment.content_type.pk,
            'object_pk': comment.object_pk
        })
    data = {'comment': 'comment comment comment'}

    with active_phase(comment.content_object.module, AskPhase):
        response = apiclient.patch(url, data, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_anonymous_user_can_not_edit_comment(comment, apiclient):
    apiclient.force_authenticate(user=None)
    url = reverse(
        'comments-detail',
        kwargs={
            'pk': comment.pk,
            'content_type': comment.content_type.pk,
            'object_pk': comment.object_pk
        })
    data = {'comment': 'comment comment comment'}

    with active_phase(comment.content_object.module, AskPhase):
        response = apiclient.patch(url, data, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_authenticated_user_can_reply_to_comment(another_user, comment,
                                                 apiclient):
    comment_contenttype = ContentType.objects.get_for_model(comment).pk

    original_url = reverse(
        'comments-detail',
        kwargs={
            'pk': comment.pk,
            'content_type': comment.content_type.pk,
            'object_pk': comment.object_pk
        })
    response = apiclient.get(original_url)
    assert len(response.data['child_comments']) == 0

    apiclient.force_authenticate(user=another_user)
    reply_url = reverse(
        'comments-list',
        kwargs={'content_type': comment_contenttype,
                'object_pk': comment.pk})
    data = {
        'comment': 'comment-reply1',
    }

    with active_phase(comment.content_object.module, AskPhase):
        response = apiclient.post(reply_url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED

    data = {
        'comment': 'comment-reply2',
    }
    with active_phase(comment.content_object.module, AskPhase):
        response = apiclient.post(reply_url, data, format='json')

    assert response.status_code == status.HTTP_201_CREATED
    response = apiclient.get(original_url)
    assert len(response.data['child_comments']) == 2
    assert 'child_comments' not in response.data['child_comments'][0]
    assert response.data['child_comments'][0]['comment'] == 'comment-reply1'
    assert response.data['child_comments'][1]['comment'] == 'comment-reply2'


@pytest.mark.django_db
def test_anonymous_user_can_not_delete_comment(comment, apiclient):
    apiclient.force_authenticate(user=None)
    url = reverse(
        'comments-detail',
        kwargs={
            'pk': comment.pk,
            'content_type': comment.content_type.pk,
            'object_pk': comment.object_pk
        })
    response = apiclient.delete(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_authenticated_user_can_not_delete_comment(comment, another_user,
                                                   apiclient):
    url = reverse(
        'comments-detail',
        kwargs={
            'pk': comment.pk,
            'content_type': comment.content_type.pk,
            'object_pk': comment.object_pk
        })
    apiclient.force_authenticate(user=another_user)
    response = apiclient.delete(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_creater_of_comment_can_set_removed_flag(comment, user, apiclient):
    url = reverse(
        'comments-detail',
        kwargs={
            'pk': comment.pk,
            'content_type': comment.content_type.pk,
            'object_pk': comment.object_pk
        })
    apiclient.force_authenticate(user=user)

    with active_phase(comment.content_object.module, AskPhase):
        response = apiclient.delete(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data['is_deleted'] is True
    assert response.data['comment'] == 'deleted by creator'


@pytest.mark.django_db
def test_admin_of_comment_can_set_censored_flag(comment, admin, apiclient):
    url = reverse(
        'comments-detail',
        kwargs={
            'pk': comment.pk,
            'content_type': comment.content_type.pk,
            'object_pk': comment.object_pk
        })
    apiclient.force_authenticate(user=admin)
    response = apiclient.delete(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['is_deleted'] is True
    assert response.data['comment'] == 'deleted by moderator'


@pytest.mark.django_db
def test_admin_of_comment_can_edit(comment, admin, apiclient):
    url = reverse(
        'comments-detail',
        kwargs={
            'pk': comment.pk,
            'content_type': comment.content_type.pk,
            'object_pk': comment.object_pk
        })
    data = {'comment': 'comment comment comment'}
    apiclient.force_authenticate(user=admin)
    response = apiclient.patch(url, data)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['comment'] == 'comment comment comment'


@pytest.mark.django_db
def test_rating_info(comment, user, another_user, apiclient):
    ct = ContentType.objects.get_for_model(comment)
    pk = comment.pk
    ratings_url = reverse(
        'ratings-list', kwargs={'content_type': ct.pk,
                                'object_pk': pk})
    apiclient.force_authenticate(user)
    data = {'value': 1}

    with active_phase(comment.content_object.module, AskPhase):
        response = apiclient.post(ratings_url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED

    comment_url = reverse(
        'comments-detail',
        kwargs={
            'pk': comment.pk,
            'content_type': comment.content_type.pk,
            'object_pk': comment.object_pk
        })
    response = apiclient.get(comment_url, format='json')
    assert response.data['ratings']['positive_ratings'] == 1
    assert response.data['ratings']['current_user_rating_value'] == 1
    apiclient.force_authenticate(another_user)
    response = apiclient.get(comment_url, format='json')
    assert response.data['ratings']['positive_ratings'] == 1
    assert response.data['ratings']['current_user_rating_value'] is None

    data = {'value': -1}
    with active_phase(comment.content_object.module, AskPhase):
        response = apiclient.post(ratings_url, data, format='json')
        response.status_code == status.HTTP_201_CREATED
    response = apiclient.get(comment_url, format='json')
    assert response.data['ratings']['positive_ratings'] == 1
    assert response.data['ratings']['current_user_rating_value'] == -1

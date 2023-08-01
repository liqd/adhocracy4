from unittest.mock import patch

import pytest
from django.contrib.contenttypes.models import ContentType
from django.test import override_settings
from django.urls import reverse
from rest_framework import status

from tests.apps.organisations.models import OrganisationTermsOfUse
from tests.apps.questions.models import Question
from tests.apps.questions.phases import AskPhase
from tests.helpers import active_phase


@pytest.mark.django_db
@pytest.fixture
def question_ct():
    return ContentType.objects.get_for_model(Question)


@pytest.mark.django_db
@override_settings(A4_USE_ORGANISATION_TERMS_OF_USE=True)
def test_agreement_save_with_comment_create(user, apiclient, question_ct, question):
    apiclient.force_authenticate(user=user)
    url = reverse(
        "comments_async-list",
        kwargs={"content_type": question_ct.pk, "object_pk": question.pk},
    )
    data = {"comment": "comment comment", "agreed_terms_of_use": True}
    with active_phase(question.module, AskPhase):
        apiclient.post(url, data, format="json")

    terms = OrganisationTermsOfUse.objects.all()
    assert len(terms) == 1
    assert terms[0].user == user


@pytest.mark.django_db
@override_settings(A4_USE_ORGANISATION_TERMS_OF_USE=True)
def test_agreement_save_with_comment_update(comment, apiclient):
    apiclient.force_authenticate(user=comment.creator)
    url = reverse(
        "comments_async-detail",
        kwargs={
            "pk": comment.pk,
            "content_type": comment.content_type.pk,
            "object_pk": comment.object_pk,
        },
    )
    data = {"comment": "comment comment comment", "agreed_terms_of_use": True}

    with active_phase(comment.content_object.module, AskPhase):
        response = apiclient.patch(url, data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["comment"] == "comment comment comment"

    terms = OrganisationTermsOfUse.objects.all()
    assert len(terms) == 1
    assert terms[0].user == comment.creator


@pytest.mark.django_db
@override_settings(A4_USE_ORGANISATION_TERMS_OF_USE=True)
def test_agreement_update_with_comment_create(
    user, apiclient, question_ct, question, organisation_terms_of_use_factory
):
    organisation_terms_of_use = organisation_terms_of_use_factory(
        user=question.creator,
        organisation=question.module.project.organisation,
        has_agreed=False,
    )
    assert not organisation_terms_of_use.has_agreed

    apiclient.force_authenticate(user=user)
    url = reverse(
        "comments_async-list",
        kwargs={"content_type": question_ct.pk, "object_pk": question.pk},
    )
    data = {"comment": "comment comment", "agreed_terms_of_use": True}
    with active_phase(question.module, AskPhase):
        apiclient.post(url, data, format="json")

    organisation_terms_of_use.refresh_from_db()
    assert organisation_terms_of_use.has_agreed


@pytest.mark.django_db
@override_settings(A4_USE_ORGANISATION_TERMS_OF_USE=True)
def test_agreement_update_with_comment_update(
    comment, apiclient, organisation_terms_of_use_factory
):
    organisation_terms_of_use = organisation_terms_of_use_factory(
        user=comment.creator,
        organisation=comment.module.project.organisation,
        has_agreed=False,
    )
    assert not organisation_terms_of_use.has_agreed
    apiclient.force_authenticate(user=comment.creator)
    url = reverse(
        "comments_async-detail",
        kwargs={
            "pk": comment.pk,
            "content_type": comment.content_type.pk,
            "object_pk": comment.object_pk,
        },
    )
    data = {"comment": "comment comment comment", "agreed_terms_of_use": True}

    with active_phase(comment.content_object.module, AskPhase):
        response = apiclient.patch(url, data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["comment"] == "comment comment comment"

    organisation_terms_of_use.refresh_from_db()
    assert organisation_terms_of_use.has_agreed


@pytest.mark.django_db
@override_settings(A4_USE_ORGANISATION_TERMS_OF_USE=True)
def test_admin_agreement_save_with_comment_update(comment, apiclient, admin):
    """Admin has to agree when updating other user's comment."""
    apiclient.force_authenticate(user=admin)
    url = reverse(
        "comments_async-detail",
        kwargs={
            "pk": comment.pk,
            "content_type": comment.content_type.pk,
            "object_pk": comment.object_pk,
        },
    )
    data = {"comment": "comment comment comment", "agreed_terms_of_use": True}

    with active_phase(comment.content_object.module, AskPhase):
        response = apiclient.patch(url, data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["comment"] == "comment comment comment"

    terms = OrganisationTermsOfUse.objects.all()
    assert len(terms) == 1
    assert terms[0].user == admin


@pytest.mark.django_db
def test_agreement_post_no_settings_no_effect(comment, apiclient):
    """Sending in post without settings should not cause agreement create."""
    apiclient.force_authenticate(user=comment.creator)
    url = reverse(
        "comments_async-detail",
        kwargs={
            "pk": comment.pk,
            "content_type": comment.content_type.pk,
            "object_pk": comment.object_pk,
        },
    )
    data = {"comment": "comment comment comment", "agreed_terms_of_use": True}

    with active_phase(comment.content_object.module, AskPhase):
        response = apiclient.patch(url, data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["comment"] == "comment comment comment"

    terms = OrganisationTermsOfUse.objects.all()
    assert len(terms) == 0


@pytest.mark.django_db
@override_settings(A4_USE_ORGANISATION_TERMS_OF_USE=True)
def test_comment_save_without_agreement_forbidden(
    user, apiclient, question_ct, question
):
    apiclient.force_authenticate(user=user)
    url = reverse(
        "comments_async-list",
        kwargs={"content_type": question_ct.pk, "object_pk": question.pk},
    )
    data = {"comment": "comment comment", "agreed_terms_of_use": False}
    with active_phase(question.module, AskPhase):
        response = apiclient.post(url, data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
@override_settings(A4_USE_ORGANISATION_TERMS_OF_USE=True)
def test_comment_save_without_agreement_data_forbidden(
    user, apiclient, question_ct, question
):
    apiclient.force_authenticate(user=user)
    url = reverse(
        "comments_async-list",
        kwargs={"content_type": question_ct.pk, "object_pk": question.pk},
    )
    data = {"comment": "comment comment"}
    with active_phase(question.module, AskPhase):
        response = apiclient.post(url, data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
@override_settings(A4_USE_ORGANISATION_TERMS_OF_USE=True)
def test_comment_save_with_already_agreed(
    user, apiclient, question_ct, question, organisation_terms_of_use_factory
):
    organisation_terms_of_use_factory(
        user=user,
        organisation=question.module.project.organisation,
        has_agreed=True,
    )
    apiclient.force_authenticate(user=user)
    url = reverse(
        "comments_async-list",
        kwargs={"content_type": question_ct.pk, "object_pk": question.pk},
    )
    data = {
        "comment": "comment comment",
    }
    with active_phase(question.module, AskPhase):
        response = apiclient.post(url, data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["comment"] == "comment comment"


@pytest.mark.django_db
@override_settings(A4_USE_ORGANISATION_TERMS_OF_USE=True)
@patch("adhocracy4.comments_async.api.reverse", return_value="/")
def test_agreement_info(
    mock_provider,
    user,
    another_user,
    apiclient,
    question_ct,
    question,
    organisation_terms_of_use_factory,
):
    organisation_terms_of_use_factory(
        user=question.creator,
        organisation=question.module.project.organisation,
        has_agreed=True,
    )
    url = reverse(
        "comments_async-list",
        kwargs={"content_type": question_ct.pk, "object_pk": question.pk},
    )

    response = apiclient.get(url)
    assert len(response.data) == 11
    assert "use_org_terms_of_use" in response.data
    assert response.data["use_org_terms_of_use"]
    assert "user_has_agreed" in response.data
    assert response.data["user_has_agreed"] is None
    assert "org_terms_url" in response.data
    assert response.data["org_terms_url"] == "/"

    # user has agreed
    apiclient.force_authenticate(user=user)
    response = apiclient.get(url)
    assert len(response.data) == 11
    assert response.data["user_has_agreed"]

    # another_user has not agreed
    apiclient.force_authenticate(user=another_user)
    response = apiclient.get(url)
    assert len(response.data) == 11
    assert not response.data["user_has_agreed"]


@pytest.mark.django_db
@override_settings(A4_USE_ORGANISATION_TERMS_OF_USE=True)
def test_agreement_info_without_terms_view_causes_error(
    apiclient, question_ct, question, organisation_terms_of_use_factory
):
    """Accessing info without organisation-terms-of-use implemented fails."""
    organisation_terms_of_use_factory(
        user=question.creator,
        organisation=question.module.project.organisation,
        has_agreed=True,
    )
    url = reverse(
        "comments_async-list",
        kwargs={"content_type": question_ct.pk, "object_pk": question.pk},
    )

    with pytest.raises(NotImplementedError):
        apiclient.get(url)


@pytest.mark.django_db
@override_settings(A4_USE_ORGANISATION_TERMS_OF_USE=True)
@patch("adhocracy4.comments_async.api.reverse", return_value="/")
def test_pagination_comment_link_with_terms(
    mock_provider, user, apiclient, question_ct, question, comment_factory
):
    url = reverse(
        "comments_async-list",
        kwargs={"content_type": question_ct.pk, "object_pk": question.pk},
    )
    url += "?commentID=no_number"
    response = apiclient.get(url)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    url = reverse(
        "comments_async-list",
        kwargs={"content_type": question_ct.pk, "object_pk": question.pk},
    )
    url += "?commentID=-1"
    response = apiclient.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert not response.data["comment_found"]
    assert response.data["use_org_terms_of_use"]
    assert response.data["user_has_agreed"] is None
    assert response.data["org_terms_url"] == "/"

    commentID = 0
    apiclient.force_authenticate(user=user)
    url = reverse(
        "comments_async-list",
        kwargs={"content_type": question_ct.pk, "object_pk": question.pk},
    )
    data = {"comment": "comment comment", "agreed_terms_of_use": True}
    with active_phase(question.module, AskPhase):
        response = apiclient.post(url, data, format="json")
        commentID = response.data["id"]
        assert commentID > 0

    url = reverse(
        "comments_async-list",
        kwargs={"content_type": question_ct.pk, "object_pk": question.pk},
    )
    url += "?commentID={}".format(commentID)
    response = apiclient.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["comment_found"]
    assert response.data["use_org_terms_of_use"]
    assert response.data["user_has_agreed"]
    assert response.data["org_terms_url"] == "/"

    comment = comment_factory(content_object=question)
    child_comment = comment_factory(content_object=comment)
    url = reverse(
        "comments_async-list",
        kwargs={"content_type": question_ct.pk, "object_pk": question.pk},
    )
    url += "?commentID={}".format(child_comment.id)
    response = apiclient.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["comment_found"]
    assert response.data["comment_parent"] == comment.id
    assert response.data["use_org_terms_of_use"]
    assert response.data["user_has_agreed"]
    assert response.data["org_terms_url"] == "/"

import pytest
from django.contrib.contenttypes.models import ContentType

from meinberlin.apps.moderatorremark.models import ModeratorRemark


@pytest.mark.django_db
def test_anonymous_cannot_add_remark(client, idea_factory):
    idea = idea_factory()
    type = ContentType.objects.get_for_model(idea)
    assert ModeratorRemark.objects.all().count() == 0
    url = "/api/contenttypes/{}/" "objects/{}/moderatorremarks/".format(
        type.id, idea.id
    )
    data = {"remark": "remark"}
    response = client.post(url, data)
    assert response.status_code == 403
    assert ModeratorRemark.objects.all().count() == 0


@pytest.mark.django_db
def test_normal_user_cannot_add_remark(apiclient, user, idea_factory):
    idea = idea_factory()
    idea.project.moderators.clear()
    type = ContentType.objects.get_for_model(idea)
    assert ModeratorRemark.objects.all().count() == 0
    assert user not in idea.project.moderators.all()
    apiclient.force_authenticate(user=user)
    url = "/api/contenttypes/{}/objects/" "{}/moderatorremarks/".format(
        type.id, idea.id
    )
    data = {"remark": "remark"}
    response = apiclient.post(url, data, format="json")
    assert response.status_code == 403
    assert ModeratorRemark.objects.all().count() == 0


@pytest.mark.django_db
def test_moderator_can_add_remark(apiclient, user, idea_factory):
    idea = idea_factory()
    idea.project.moderators.add(user)
    type = ContentType.objects.get_for_model(idea)
    assert ModeratorRemark.objects.all().count() == 0
    assert user in idea.project.moderators.all()
    apiclient.force_authenticate(user=user)
    url = "/api/contenttypes/{}/objects/" "{}/moderatorremarks/".format(
        type.id, idea.id
    )
    data = {"remark": "remark"}
    response = apiclient.post(url, data, format="json")
    assert response.status_code == 201
    assert ModeratorRemark.objects.all().count() == 1


@pytest.mark.django_db
def test_initiator_can_add_remark(apiclient, user, idea_factory):
    idea = idea_factory()
    idea.project.organisation.initiators.add(user)
    type = ContentType.objects.get_for_model(idea)
    assert ModeratorRemark.objects.all().count() == 0
    assert user in idea.project.organisation.initiators.all()
    apiclient.force_authenticate(user=user)
    url = "/api/contenttypes/{}/objects/" "{}/moderatorremarks/".format(
        type.id, idea.id
    )
    data = {"remark": "remark"}
    response = apiclient.post(url, data, format="json")
    assert response.status_code == 201
    assert ModeratorRemark.objects.all().count() == 1


@pytest.mark.django_db
def test_admin_can_add_remark(apiclient, admin, idea_factory):
    idea = idea_factory()
    type = ContentType.objects.get_for_model(idea)
    assert ModeratorRemark.objects.all().count() == 0
    assert admin not in idea.project.organisation.initiators.all()
    assert admin not in idea.project.moderators.all()
    apiclient.force_authenticate(user=admin)
    url = "/api/contenttypes/{}/objects/" "{}/moderatorremarks/".format(
        type.id, idea.id
    )
    data = {"remark": "remark"}
    response = apiclient.post(url, data, format="json")
    assert response.status_code == 201
    assert ModeratorRemark.objects.all().count() == 1


@pytest.mark.django_db
def test_anonymous_can_not_edit_remark(apiclient, moderator_remark_factory):
    remark = moderator_remark_factory()
    assert ModeratorRemark.objects.all().count() == 1
    remark.item.project.moderators.clear()
    content_type = ContentType.objects.get_for_model(remark.item)
    url = "/api/contenttypes/{}/objects/{}" "/moderatorremarks/{}/".format(
        content_type.id, remark.item.id, remark.id
    )
    data = {"remark": "remark"}
    response = apiclient.put(url, data, format="json")
    assert response.status_code == 403
    assert ModeratorRemark.objects.all().count() == 1


@pytest.mark.django_db
def test_normal_user_can_not_edit_remark(apiclient, user, moderator_remark_factory):
    remark = moderator_remark_factory()
    assert ModeratorRemark.objects.all().count() == 1
    remark.item.project.moderators.clear()
    content_type = ContentType.objects.get_for_model(remark.item)
    assert user not in remark.item.project.moderators.all()
    apiclient.force_authenticate(user=user)
    url = "/api/contenttypes/{}/objects/" "{}/moderatorremarks/{}/".format(
        content_type.id, remark.item.id, remark.id
    )
    data = {"remark": "remark"}
    response = apiclient.put(url, data, format="json")
    assert response.status_code == 403
    assert ModeratorRemark.objects.all().count() == 1


@pytest.mark.django_db
def test_moderator_can_edit_remark(apiclient, user, moderator_remark_factory):
    remark = moderator_remark_factory()
    assert ModeratorRemark.objects.all().count() == 1
    remark.item.project.moderators.add(user)
    content_type = ContentType.objects.get_for_model(remark.item)
    assert user in remark.item.project.moderators.all()
    apiclient.force_authenticate(user=user)
    url = "/api/contenttypes/{}/objects/" "{}/moderatorremarks/{}/".format(
        content_type.id, remark.item.id, remark.id
    )
    data = {"remark": "remark"}
    response = apiclient.put(url, data, format="json")
    assert response.status_code == 200
    assert ModeratorRemark.objects.all().count() == 1


@pytest.mark.django_db
def test_initiator_can_edit_remark(apiclient, user, moderator_remark_factory):
    remark = moderator_remark_factory()
    assert ModeratorRemark.objects.all().count() == 1
    remark.item.project.organisation.initiators.add(user)
    content_type = ContentType.objects.get_for_model(remark.item)
    assert user not in remark.item.project.moderators.all()
    assert user in remark.item.project.organisation.initiators.all()
    apiclient.force_authenticate(user=user)
    url = "/api/contenttypes/{}/objects/" "{}/moderatorremarks/{}/".format(
        content_type.id, remark.item.id, remark.id
    )
    data = {"remark": "remark updated"}
    response = apiclient.put(url, data, format="json")
    assert response.status_code == 200
    assert ModeratorRemark.objects.all().count() == 1
    assert ModeratorRemark.objects.all().first().remark == "remark updated"

    @pytest.mark.django_db
    def test_admin_can_edit_remark(apiclient, admin, moderator_remark_factory):
        remark = moderator_remark_factory()
        assert ModeratorRemark.objects.all().count() == 1
        content_type = ContentType.objects.get_for_model(remark.item)
        assert admin not in remark.item.project.moderators.all()
        assert admin not in remark.item.project.organisation.initiators.all()
        apiclient.force_authenticate(user=admin)
        url = "/api/contenttypes/{}/objects/" "{}/moderatorremarks/{}/".format(
            content_type.id, remark.item.id, remark.id
        )
        data = {"remark": "remark updated"}
        response = apiclient.put(url, data, format="json")
        assert response.status_code == 200
        assert ModeratorRemark.objects.all().count() == 1
        assert ModeratorRemark.objects.all().first().remark == "remark updated"

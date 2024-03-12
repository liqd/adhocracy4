import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from adhocracy4.test.helpers import redirect_target
from meinberlin.test.helpers import setup_group_members


@pytest.mark.django_db
def test_upload_image_not_allowed_unauthenticated(client):
    file = SimpleUploadedFile("test_image_should_not_exist.png", b"random image data")
    data = {
        "upload": file,
    }
    url = reverse("ck_editor_5_upload_file")
    r = client.post(url, data)
    assert r.status_code == 302
    assert redirect_target(r) == "account_login"


@pytest.mark.django_db
def test_upload_image_not_allowed_normal_user(client, user):
    client.force_login(user)
    file = SimpleUploadedFile("test_image_should_not_exist.png", b"random image data")
    data = {
        "upload": file,
    }
    url = reverse("ck_editor_5_upload_file")
    r = client.post(url, data)
    assert r.status_code == 302
    assert redirect_target(r) == "account_login"


@pytest.mark.django_db
def test_upload_image_allowed_admin(client, admin):
    client.force_login(admin)
    file = SimpleUploadedFile("test_image.png", b"random image data")
    data = {
        "upload": file,
    }
    url = reverse("ck_editor_5_upload_file")
    r = client.post(url, data)
    assert r.status_code == 200


@pytest.mark.django_db
def test_upload_image_allowed_initiator(client, organisation):
    initiator = organisation.initiators.first()
    client.force_login(initiator)
    file = SimpleUploadedFile("test_image.png", b"random image data")
    data = {
        "upload": file,
    }
    url = reverse("ck_editor_5_upload_file")
    r = client.post(url, data)
    assert r.status_code == 200


@pytest.mark.django_db
def test_upload_image_allowed_group_member(
    client, project, group_factory, user_factory
):
    (
        project,
        group_member_in_org,
        group_member_in_pro,
        group_member_out,
    ) = setup_group_members(project, group_factory, user_factory)
    client.force_login(group_member_in_org)
    file = SimpleUploadedFile("test_image.png", b"random image data")
    data = {
        "upload": file,
    }
    url = reverse("ck_editor_5_upload_file")
    r = client.post(url, data)
    assert r.status_code == 200
    client.force_login(group_member_in_pro)
    file = SimpleUploadedFile("test_image.png", b"random image data")
    data = {
        "upload": file,
    }
    url = reverse("ck_editor_5_upload_file")
    r = client.post(url, data)
    assert r.status_code == 200
    client.force_login(group_member_out)
    file = SimpleUploadedFile("test_image.png", b"random image data")
    data = {
        "upload": file,
    }
    url = reverse("ck_editor_5_upload_file")
    r = client.post(url, data)
    assert r.status_code == 200

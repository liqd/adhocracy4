import importlib
from pathlib import Path

import pytest
from django.test.utils import override_settings
from django.urls import reverse

from adhocracy4.modules.models import Module
from adhocracy4.projects.models import Project
from adhocracy4.test.helpers import assert_template_response
from adhocracy4.test.helpers import redirect_target


@pytest.mark.django_db
def test_project_list(client, organisation, project_factory, user, another_user):
    project0 = project_factory(organisation=organisation)
    project1 = project_factory(organisation=organisation)

    organisation.initiators.add(another_user)

    project_list_url = reverse(
        "a4dashboard:project-list", kwargs={"organisation_slug": organisation.slug}
    )
    response = client.get(project_list_url)
    assert redirect_target(response) == "account_login"

    client.login(username=user, password="password")
    response = client.get(project_list_url)
    assert response.status_code == 403

    client.login(username=another_user, password="password")
    response = client.get(project_list_url)
    assert_template_response(response, "a4dashboard/project_list.html")

    project_list = response.context_data["project_list"]
    assert list(project_list) == [project1, project0]


@pytest.mark.django_db
def test_blueprint_list(client, organisation, user, another_user):
    blueprint_list_url = reverse(
        "a4dashboard:blueprint-list", kwargs={"organisation_slug": organisation.slug}
    )
    response = client.get(blueprint_list_url)
    assert redirect_target(response) == "account_login"

    client.login(username=user, password="password")
    response = client.get(blueprint_list_url)
    assert response.status_code == 403

    organisation.initiators.add(another_user)
    client.login(username=another_user, password="password")
    response = client.get(blueprint_list_url)
    assert_template_response(response, "a4dashboard/blueprint_list.html")

    view = response.context_data["view"]
    assert 1 == len(view.blueprints)
    assert "questions" == view.blueprints[0][0]


@pytest.mark.django_db
def test_project_create(client, organisation, user_factory, group_factory):
    group1 = group_factory()
    group2 = group_factory()
    user = user_factory()
    initiator = user_factory()
    group_member = user_factory.create(groups=(group1, group2))
    organisation.groups.add(group2)

    project_create_url = reverse(
        "a4dashboard:project-create",
        kwargs={"organisation_slug": organisation.slug, "blueprint_slug": "questions"},
    )

    data = {"name": "project name", "description": "project description"}

    response = client.post(project_create_url, data)
    assert redirect_target(response) == "account_login"

    client.login(username=user, password="password")
    response = client.post(project_create_url, data)
    assert response.status_code == 403

    organisation.initiators.add(initiator)
    client.login(username=initiator, password="password")
    response = client.post(project_create_url, data)
    assert redirect_target(response) == "project-edit"

    assert 1 == Project.objects.all().count()
    project = Project.objects.all().first()
    assert "project name" == project.name
    assert "project description" == project.description

    client.login(username=group_member, password="password")
    response = client.post(project_create_url, data)
    assert redirect_target(response) == "project-edit"

    assert 2 == Project.objects.all().count()
    assert 1 == Project.objects.filter(group_id=group2.id).count()


@override_settings(A4_BLUEPRINT_TYPES=[("QS", "questions")])
@override_settings(
    A4_DASHBOARD={"BLUEPRINTS": "tests.project.blueprints_with_type.blueprints"}
)
@pytest.mark.django_db
def test_project_create_with_blueprint_type(client, organisation, user_factory):
    # reload blueprints to reinitialize ProjectBlueprint with
    # overridden settings
    bp_module = importlib.import_module("adhocracy4.dashboard.blueprints")
    importlib.reload(bp_module)

    initiator = user_factory()
    organisation.initiators.add(initiator)

    project_create_url = reverse(
        "a4dashboard:project-create",
        kwargs={"organisation_slug": organisation.slug, "blueprint_slug": "questions"},
    )

    data = {"name": "project name", "description": "project description"}

    client.login(username=initiator, password="password")
    response = client.post(project_create_url, data)
    assert redirect_target(response) == "project-edit"

    assert 1 == Project.objects.all().count()
    project = Project.objects.all().first()
    assert "project name" == project.name
    assert "project description" == project.description

    assert 1 == Module.objects.all().count()
    assert Module.objects.first().blueprint_type == "QS"


@pytest.mark.django_db
def test_project_edit_redirect(client, project):
    project_edit_url = reverse(
        "a4dashboard:project-edit", kwargs={"project_slug": project.slug}
    )

    response = client.get(project_edit_url)
    assert response.status_code == 302
    assert response["location"].startswith("/dashboard")


@pytest.mark.django_db
def test_project_publish_perms(client, phase, user, another_user):
    project = phase.module.project

    project_publish_url = reverse(
        "a4dashboard:project-publish", kwargs={"project_slug": project.slug}
    )

    data = {"action": "publish"}

    response = client.post(project_publish_url, data)
    assert redirect_target(response) == "account_login"

    client.login(username=user, password="password")
    response = client.post(project_publish_url, data)
    assert response.status_code == 403

    organisation = project.organisation
    organisation.initiators.add(another_user)
    client.login(username=another_user, password="password")
    response = client.post(project_publish_url, data)
    assert redirect_target(response) == "project-edit"


@pytest.mark.django_db
def test_project_publish(client, phase, another_user):
    project = phase.module.project
    project.is_draft = True
    project.information = ""
    project.save()
    organisation = project.organisation
    organisation.initiators.add(another_user)

    project_publish_url = reverse(
        "a4dashboard:project-publish", kwargs={"project_slug": project.slug}
    )

    data = {"action": "publish"}

    # publishing incomplete projects has no effect
    client.login(username=another_user, password="password")
    response = client.post(project_publish_url, data)
    assert redirect_target(response) == "project-edit"

    project.refresh_from_db()
    assert project.is_draft is True

    # complete project and publish it
    project.information = "project information"
    project.save()

    client.login(username=another_user, password="password")
    response = client.post(project_publish_url, data)
    assert redirect_target(response) == "project-edit"

    project.refresh_from_db()
    assert project.is_draft is False


@pytest.mark.django_db
def test_project_unpublish(client, phase, another_user):
    project = phase.module.project
    project.is_draft = False
    project.save()
    organisation = project.organisation
    organisation.initiators.add(another_user)

    project_publish_url = reverse(
        "a4dashboard:project-publish", kwargs={"project_slug": project.slug}
    )

    data = {"action": "unpublish"}

    client.login(username=another_user, password="password")
    response = client.post(project_publish_url, data)
    assert redirect_target(response) == "project-edit"

    project.refresh_from_db()
    assert project.is_draft is True

    # unpublishing draft projects has no effect
    client.login(username=another_user, password="password")
    response = client.post(project_publish_url, data)
    assert redirect_target(response) == "project-edit"

    project.refresh_from_db()
    assert project.is_draft is True


@pytest.mark.django_db
def test_project_publish_redirect(client, project, another_user):
    project_publish_url = reverse(
        "a4dashboard:project-publish", kwargs={"project_slug": project.slug}
    )

    organisation = project.organisation
    organisation.initiators.add(another_user)

    client.login(username=another_user, password="password")

    response = client.post(project_publish_url, {"referrer": "refurl"})
    assert response.status_code == 302
    assert response["location"] == "refurl"

    response = client.post(project_publish_url, {}, HTTP_REFERER="refurl")
    assert response.status_code == 302
    assert response["location"] == "refurl"

    response = client.post(project_publish_url, {})
    assert redirect_target(response) == "project-edit"


@pytest.mark.django_db
def test_project_duplicate(
    client, another_user, area_settings, phase_factory, image_factory, topic_factory
):
    module = area_settings.module
    project = module.project
    test_image = image_factory((1500, 500), "JPEG")
    test_tile_image = image_factory((300, 150), "JPEG")
    organisation = project.organisation
    organisation.initiators.add(another_user)
    phase = phase_factory(module=module)

    project.is_draft = False
    project.is_archived = True

    project.tile_image = test_tile_image
    project.image = test_image
    topic_factory(projects=[project])
    project.save()

    project_list_url = reverse(
        "a4dashboard:project-list", kwargs={"organisation_slug": organisation.slug}
    )

    client.login(username=another_user, password="password")
    response = client.post(
        project_list_url, {"duplicate": "1", "project_pk": project.pk}
    )
    assert response.status_code == 302

    assert Project.objects.all().count() == 2

    project_clone = Project.objects.order_by("pk").last()
    assert project_clone.pk != project.pk

    assert project_clone.is_draft is True
    assert project_clone.is_archived is False
    assert project_clone.topics.all().exists()
    assert len(project_clone.topics.all()) == len(project.topics.all())

    assert project_clone.image
    # django saves a new instance of the image by extending the original name
    assert Path(project.image.name).stem in Path(project_clone.image.name).stem
    assert len(project_clone.image.name) > len(project.image.name)
    assert Path(project_clone.image.path).parent == Path(project.image.path).parent

    assert project_clone.tile_image
    assert (
        Path(project.tile_image.name).stem in Path(project_clone.tile_image.name).stem
    )
    assert len(project_clone.tile_image.name) > len(project.tile_image.name)
    assert (
        Path(project_clone.tile_image.path).parent
        == Path(project.tile_image.path).parent
    )

    assert project_clone.created > project.created
    for attr in ("description", "information", "result", "access"):
        assert getattr(project_clone, attr) == getattr(project, attr)
    for moderator in project.moderators.all():
        assert moderator in project.moderators.all()

    module_clone = project_clone.module_set.first()
    assert module_clone.pk != module.pk
    for attr in ("name", "description", "weight"):
        assert getattr(module_clone, attr) == getattr(module, attr)

    phase_clone = module_clone.phase_set.first()
    assert phase_clone.pk != phase.pk
    for attr in ("name", "description", "type", "start_date", "end_date", "weight"):
        assert getattr(phase_clone, attr) == getattr(phase, attr)

    area_settings_clone = module_clone.settings_instance
    assert area_settings_clone.pk != area_settings.pk
    assert area_settings_clone.polygon == area_settings.polygon

    # check if original project is deleted, the copied image remains
    project.delete()
    project_clone.refresh_from_db()
    assert project_clone.tile_image.path is not None

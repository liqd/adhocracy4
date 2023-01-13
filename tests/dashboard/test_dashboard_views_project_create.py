import pytest
from django.urls import reverse

from adhocracy4.projects.models import Project
from adhocracy4.test.helpers import redirect_target


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
        kwargs={
            "organisation_slug": organisation.slug,
        },
    )

    data = {"name": "project name", "description": "project description", "access": 1}

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

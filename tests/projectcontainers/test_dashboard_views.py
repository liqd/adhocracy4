import pytest
from django.urls import reverse

from adhocracy4.projects.models import Project
from adhocracy4.test.helpers import redirect_target
from meinberlin.apps.projectcontainers.models import ProjectContainer


@pytest.mark.django_db
def test_container_create(
        client, organisation, user_factory, group_factory, admin):
    group1 = group_factory()
    group2 = group_factory()
    user = user_factory()
    initiator = user_factory()
    group_member = user_factory.create(groups=(group1, group2))
    organisation.groups.add(group2)

    project_create_url = reverse('a4dashboard:container-create', kwargs={
        'organisation_slug': organisation.slug,
    })

    data = {
        'name': 'container name',
        'description': 'container description'
    }

    response = client.post(project_create_url, data)
    assert redirect_target(response) == 'account_login'

    client.login(username=user, password='password')
    response = client.post(project_create_url, data)
    assert response.status_code == 403

    organisation.initiators.add(initiator)
    client.login(username=initiator, password='password')
    response = client.post(project_create_url, data)
    assert response.status_code == 403

    client.login(username=admin, password='password')
    response = client.post(project_create_url, data)
    assert redirect_target(response) == 'project-edit'

    assert 1 == Project.objects.all().count()
    project = Project.objects.all().first()
    assert 'container name' == project.name
    assert 'container description' == project.description

    client.login(username=group_member, password='password')
    response = client.post(project_create_url, data)
    assert response.status_code == 403

    assert 1 == Project.objects.all().count()
    assert 0 == Project.objects.filter(group_id=group2.id).count()
    assert 1 == ProjectContainer.objects.all().count()
    assert 0 == ProjectContainer.objects.filter(group_id=group2.id).count()

import pytest
from django.core.urlresolvers import reverse


@pytest.mark.django_db
def test_hide_private_projects(client, user, project_factory):
    public = project_factory()
    private = project_factory(is_public=False)

    client.login(username=user, password='password')
    url = reverse('project-list')
    response = client.get(url)
    assert response.status_code == 200

    project_list = response.context['project_list']
    assert public in project_list
    assert private not in project_list


@pytest.mark.django_db
def test_show_private_projects_participant(client, user, project_factory):
    public = project_factory()
    private = project_factory(is_public=False)
    private.participants.add(user)

    client.login(username=user, password='password')
    url = reverse('project-list')
    response = client.get(url)
    assert response.status_code == 200

    project_list = response.context['project_list']
    assert public in project_list
    assert private in project_list


@pytest.mark.django_db
def test_show_private_projects_initiators(client, user, project_factory):
    public = project_factory()
    private = project_factory(is_public=False)
    private.organisation.initiators.add(user)

    client.login(username=user, password='password')
    url = reverse('project-list')
    response = client.get(url)
    assert response.status_code == 200

    project_list = response.context['project_list']
    assert public in project_list
    assert private in project_list

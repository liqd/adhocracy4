import pytest
from django.urls import reverse

from adhocracy4.projects.enums import Access
from adhocracy4.test.helpers import redirect_target


@pytest.mark.django_db
def test_detail_view(client, project):
    project_url = reverse('project-detail', args=[project.slug])
    response = client.get(project_url)
    assert response.status_code == 200
    assert response.context_data['view'].project == project


@pytest.mark.django_db
@pytest.mark.parametrize('project__access', [Access.PRIVATE])
def test_detail_private_project(client, project, user):
    project_url = reverse('project-detail', args=[project.slug])
    response = client.get(project_url)
    assert response.status_code == 302
    assert redirect_target(response) == 'account_login'

    client.login(username=user, password='password')
    response = client.get(project_url)
    assert response.status_code == 403

    project.participants.add(user)
    response = client.get(project_url)
    assert response.status_code == 200
    assert response.context_data['view'].project == project


@pytest.mark.django_db
@pytest.mark.parametrize('project__is_draft', [True])
def test_detail_draft_project(client, project, user, another_user):
    project_url = reverse('project-detail', args=[project.slug])
    organisation = project.organisation
    organisation.initiators.add(another_user)
    response = client.get(project_url)
    assert response.status_code == 302
    assert redirect_target(response) == 'account_login'

    client.login(username=user, password='password')
    response = client.get(project_url)
    assert response.status_code == 403

    client.login(username=another_user, password='password')
    response = client.get(project_url)
    assert response.status_code == 200
    assert response.context_data['view'].project == project

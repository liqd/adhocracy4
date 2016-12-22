import pytest
from django.core.urlresolvers import reverse
from tests.helpers import redirect_target


@pytest.mark.django_db
def test_detail_view(client, project):
    project_url = reverse('project-detail', args=[project.slug])
    response = client.get(project_url)
    assert response.status_code == 200
    assert response.context_data['view'].project == project


@pytest.mark.django_db
@pytest.mark.parametrize('project__is_public', [False])
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
def test_detail_draft_project(client, project, user, staff_user):
    project_url = reverse('project-detail', args=[project.slug])
    response = client.get(project_url)
    assert response.status_code == 302
    assert redirect_target(response) == 'account_login'

    client.login(username=user, password='password')
    response = client.get(project_url)
    assert response.status_code == 403

    client.login(username=staff_user, password='password')
    response = client.get(project_url)
    assert response.status_code == 200
    assert response.context_data['view'].project == project

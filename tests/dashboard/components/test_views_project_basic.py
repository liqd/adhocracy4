import pytest

from adhocracy4.dashboard import components
from adhocracy4.projects.enums import Access
from adhocracy4.test.helpers import redirect_target

component = components.projects.get('basic')


@pytest.mark.django_db
def test_edit_view(client, project, admin):
    url = component.get_base_url(project)
    client.login(username=admin.username, password='password')
    response = client.get(url)
    assert response.status_code == 200

    data = {
        'name': 'name',
        'description': 'desc',
        'image_copyright': 'copyright',
        'tile_image_copyright': 'tile_copyright',
        'is_archived': False,
        'access': Access.SEMIPUBLIC.value,
    }
    response = client.post(url, data)
    assert redirect_target(response) == 'dashboard-basic-edit'
    project.refresh_from_db()
    assert project.name == data.get('name')
    assert project.description == data.get('description')
    assert project.tile_image_copyright == \
        data.get('tile_image_copyright')
    assert project.is_archived == data.get('is_archived')
    assert project.access == data.get('access')

import pytest

from adhocracy4.dashboard import components
from adhocracy4.test.helpers import redirect_target

component = components.modules.get('module_basic')


@pytest.mark.django_db
def test_edit_view(client, project, module_factory,
                   phase_factory, admin):
    module = module_factory(project=project)
    phase_factory(module=module)
    url = component.get_base_url(module)
    client.login(username=admin.username, password='password')
    response = client.get(url)
    assert response.status_code == 200

    data = {
        'name': 'name',
        'description': 'desc',
    }
    response = client.post(url, data)
    assert redirect_target(response) == 'dashboard-module_basic-edit'
    module.refresh_from_db()
    assert module.name == data.get('name')
    assert module.description == data.get('description')

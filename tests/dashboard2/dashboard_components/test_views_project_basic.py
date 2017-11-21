import pytest

from meinberlin.apps.dashboard2 import components
from meinberlin.test.helpers import assert_dashboard_form_component_edited
from meinberlin.test.helpers import assert_dashboard_form_component_response

component = components.projects.get('basic')


@pytest.mark.django_db
def test_edit_view(client, project):
    initiator = project.organisation.initiators.first()
    url = component.get_base_url(project)
    client.login(username=initiator.email, password='password')
    response = client.get(url)
    assert_dashboard_form_component_response(response, component)

    data = {
        'name': 'name',
        'description': 'desc',
        'image_copyright': 'coryright',
        'tile_image_copyright': 'tile_copyright',
        'is_archived': True,
        'is_public': True,
    }
    response = client.post(url, data)
    assert_dashboard_form_component_edited(response, component, project, data)

import json

import pytest

from adhocracy4.dashboard import components
from adhocracy4.test.helpers import redirect_target

component = components.modules.get('area_settings')


@pytest.mark.django_db
def test_edit_view(client, project, module_factory,
                   phase_factory, admin, area_settings):
    module = area_settings.module
    phase_factory(module=module)
    url = component.get_base_url(module)
    client.login(username=admin.username, password='password')
    response = client.get(url)
    assert response.status_code == 200

    data = {
        'polygon': '{"type":"FeatureCollection", "features":[{"type":'
                   '"Feature", "properties":{}, "geometry": {"type":"Polygon",'
                   '"coordinates":[[[13.0,52.0], [13.0,53.0], [14.0,52.0],'
                   '[14.0,53.0]]]}}]}'
    }
    response = client.post(url, data)
    assert redirect_target(response) == 'dashboard-area_settings-edit'
    area_settings.refresh_from_db()
    assert area_settings.polygon == json.loads(data.get('polygon'))

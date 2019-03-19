import json

import pytest

from adhocracy4.dashboard import components
from adhocracy4.dashboard.dashboard import ModuleAreaSettingsComponent


@pytest.mark.django_db
def test_module_area_settings(area_settings):
    module = area_settings.module

    component = ModuleAreaSettingsComponent()
    assert component.is_effective(module) is True
    assert component.get_progress(module) == (1, 1)

    area_settings.polygon = {}
    area_settings.save()
    assert component.get_progress(module) == (0, 1)


@pytest.mark.django_db
def test_module_area_settings_view(client, area_settings, phase_factory,
                                   user):
    module = area_settings.module
    phase_factory(module=module)
    organisation = module.project.organisation

    organisation.initiators.add(user)
    organisation.save()

    component = components.modules.get('area_settings')
    component_url = component.get_base_url(module)

    client.login(username=user.username, password='password')
    response = client.get(component_url)
    assert response.status_code == 200

    data = {
        'polygon': '{"type":"FeatureCollection", "features":[{"type":'
                   '"Feature", "properties":{}, "geometry": {"type":"Polygon",'
                   '"coordinates":[[[13.0,52.0], [13.0,53.0], [14.0,52.0],'
                   '[14.0,53.0]]]}}]}'
    }
    response = client.post(component_url, data)
    assert response.status_code == 302
    assert response['location'] == component_url

    area_settings.refresh_from_db()
    assert area_settings.polygon == json.loads(data.get('polygon'))

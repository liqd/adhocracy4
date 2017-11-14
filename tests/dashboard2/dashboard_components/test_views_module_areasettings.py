import json

import pytest

from adhocracy4.test.helpers import redirect_target
from meinberlin.apps.dashboard2 import components
from meinberlin.apps.ideas.phases import CollectFeedbackPhase
from meinberlin.test.helpers import assert_dashboard_form_component_response
from meinberlin.test.helpers import setup_phase

component = components.modules.get('area_settings')


@pytest.mark.django_db
def test_edit_view(client, phase_factory, area_settings_factory):
    phase, module, project, item = setup_phase(
        phase_factory, None, CollectFeedbackPhase)
    area_settings = area_settings_factory(module=module)
    initiator = module.project.organisation.initiators.first()
    url = component.get_base_url(module)
    client.login(username=initiator.email, password='password')
    response = client.get(url)
    assert_dashboard_form_component_response(response, component)

    data = {
        'polygon': '{"type":"FeatureCollection", "features":[{"type":'
                   '"Feature", "properties":{}, "geometry": {"type":"Polygon",'
                   '"coordinates":[[[13.0,52.0], [13.0,53.0], [14.0,52.0],'
                   '[14.0,53.0]]]}}]}'
    }
    response = client.post(url, data)
    assert redirect_target(response) == \
        'dashboard-{}-edit'.format(component.identifier)
    area_settings.refresh_from_db()
    assert area_settings.polygon == json.loads(data.get('polygon'))

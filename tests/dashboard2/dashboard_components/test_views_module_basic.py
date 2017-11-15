import pytest

from meinberlin.apps.dashboard2 import components
from meinberlin.apps.ideas.phases import CollectFeedbackPhase
from meinberlin.test.helpers import assert_dashboard_form_component_edited
from meinberlin.test.helpers import assert_dashboard_form_component_response
from meinberlin.test.helpers import setup_phase

component = components.modules.get('module_basic')


@pytest.mark.django_db
def test_edit_view(client, phase_factory):
    phase, module, project, item = setup_phase(
        phase_factory, None, CollectFeedbackPhase)
    initiator = module.project.organisation.initiators.first()
    url = component.get_base_url(module)
    client.login(username=initiator.email, password='password')
    response = client.get(url)
    assert_dashboard_form_component_response(response, component)

    data = {
        'name': 'name',
        'description': 'desc',
    }
    response = client.post(url, data)
    assert_dashboard_form_component_edited(response, component, module, data)

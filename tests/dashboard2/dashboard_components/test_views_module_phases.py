import pytest
from dateutil.parser import parse

from adhocracy4.test.helpers import redirect_target
from meinberlin.apps.dashboard2 import components
from meinberlin.apps.ideas.phases import CollectFeedbackPhase
from meinberlin.test.helpers import assert_dashboard_form_component_response
from meinberlin.test.helpers import setup_phase

component = components.modules.get('phases')


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
        'phase_set-TOTAL_FORMS': 1,
        'phase_set-INITIAL_FORMS': 1,
        'phase_set-0-id': phase.pk,
        'phase_set-0-module': module.pk,
        'phase_set-0-name': 'name',
        'phase_set-0-description': 'desc',
        'phase_set-0-start_date_0': '2013-01-01',
        'phase_set-0-start_date_1': '18:00',
        'phase_set-0-end_date_0': '2013-01-10',
        'phase_set-0-end_date_1': '18:00',
        'phase_set-0-type': 'meinberlin_ideas:050:collect_feedback',

    }
    response = client.post(url, data)
    phase.refresh_from_db()
    assert redirect_target(response) == \
        'dashboard-{}-edit'.format(component.identifier)
    assert phase.name == data.get('phase_set-0-name')
    assert phase.description == data.get('phase_set-0-description')
    assert phase.start_date == parse("2013-01-01 17:00:00 UTC")
    assert phase.end_date == parse("2013-01-10 17:00:00 UTC")

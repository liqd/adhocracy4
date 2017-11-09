import pytest

from meinberlin.apps.dashboard2 import components
from meinberlin.apps.polls.phases import VotingPhase
from tests.helpers import assert_template_response
from tests.helpers import setup_phase

component = components.modules.get('polls')


@pytest.mark.django_db
def test_edit_view(client, phase_factory):
    phase, module, project, item = setup_phase(
        phase_factory, None, VotingPhase)
    initiator = module.project.organisation.initiators.first()
    url = component.get_base_url(module)
    client.login(username=initiator.email, password='password')
    response = client.get(url)
    assert_template_response(
        response, 'meinberlin_polls/poll_dashboard.html')

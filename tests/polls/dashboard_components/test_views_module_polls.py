import pytest

from adhocracy4.dashboard import components
from adhocracy4.polls.phases import VotingPhase
from adhocracy4.test.helpers import assert_template_response
from adhocracy4.test.helpers import setup_phase

component = components.modules.get('polls')


@pytest.mark.django_db
def test_edit_view(client, phase_factory, user_factory):
    phase, module, project, item = setup_phase(
        phase_factory, None, VotingPhase)
    initiator = user_factory()
    project.organisation.initiators.add(initiator)
    url = component.get_base_url(module)
    client.login(username=initiator.username, password='password')
    response = client.get(url)
    assert_template_response(response, 'a4polls/poll_dashboard.html')
    assert response.template_name[0] == 'a4polls/poll_dashboard.html'

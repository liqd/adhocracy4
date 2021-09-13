import pytest

from adhocracy4.dashboard import components
from adhocracy4.test.helpers import assert_template_response
from adhocracy4.test.helpers import setup_phase
from meinberlin.apps.ideas.phases import CollectFeedbackPhase

component = components.projects.get('adminlog')


@pytest.mark.django_db
def test_edit_view(client, phase_factory):
    phase, module, project, item = setup_phase(
        phase_factory, None, CollectFeedbackPhase)
    initiator = module.project.organisation.initiators.first()
    url = component.get_base_url(project)
    client.login(username=initiator.email, password='password')
    response = client.get(url)
    assert_template_response(
        response, 'meinberlin_adminlog/project_adminlog_dashboard.html')

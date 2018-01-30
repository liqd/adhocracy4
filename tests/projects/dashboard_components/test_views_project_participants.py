import pytest

from adhocracy4.dashboard import components
from adhocracy4.test.helpers import redirect_target
from meinberlin.apps.ideas.phases import CollectFeedbackPhase
from meinberlin.apps.projects.models import ParticipantInvite
from meinberlin.test.helpers import assert_template_response
from meinberlin.test.helpers import setup_phase

component = components.projects.get('participants')


@pytest.mark.django_db
def test_edit_view(client, phase_factory):
    phase, module, project, idea = setup_phase(
        phase_factory, None, CollectFeedbackPhase)
    initiator = module.project.organisation.initiators.first()
    url = component.get_base_url(project)
    client.login(username=initiator.email, password='password')
    response = client.get(url)
    assert_template_response(
        response, 'meinberlin_projects/project_participants.html')

    data = {
        'add_users': 'test1@foo.bar,test2@foo.bar',
    }
    response = client.post(url, data)
    assert redirect_target(response) == \
        'dashboard-{}-edit'.format(component.identifier)
    assert ParticipantInvite.objects.get(email='test1@foo.bar')
    assert ParticipantInvite.objects.get(email='test2@foo.bar')

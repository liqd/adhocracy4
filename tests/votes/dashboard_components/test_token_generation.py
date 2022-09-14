import pytest
from background_task.models import Task

from adhocracy4.dashboard import components
from adhocracy4.test.helpers import redirect_target
from adhocracy4.test.helpers import setup_phase
from meinberlin.apps.budgeting.phases import VotingPhase

component = components.modules.get('voting_token_generation')


@pytest.mark.django_db
def test_token_generate_view(client, phase_factory, module_factory,
                             voting_token_factory):
    phase, module, project, item = setup_phase(
        phase_factory, None, VotingPhase)
    other_module = module_factory()
    voting_token_factory(module=module)
    voting_token_factory(module=module)
    voting_token_factory(module=module, is_active=False)
    voting_token_factory(module=other_module)

    initiator = module.project.organisation.initiators.first()
    url = component.get_base_url(module)
    client.login(username=initiator.email, password='password')
    response = client.get(url)
    assert response.status_code == 200
    assert 'number_of_module_tokens' in response.context
    number_of_module_tokens = response.context['number_of_module_tokens']
    assert number_of_module_tokens == 2
    data = {
        'number_of_tokens': 12
    }
    response = client.post(url, data)
    assert redirect_target(response) == 'voting-token-generation'
    assert Task.objects.all().count() == 1
    task = Task.objects.first()
    assert task.task_name == \
        'meinberlin.apps.votes.tasks.generate_voting_tokens_batch'
    assert task.task_params == '[[' + str(module.id) + ', 12], {}]'

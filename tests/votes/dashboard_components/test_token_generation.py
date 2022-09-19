from unittest.mock import patch

import pytest
from background_task.models import Task
from django.contrib.messages import get_messages
from django.utils import translation

from adhocracy4.dashboard import components
from adhocracy4.test.helpers import redirect_target
from adhocracy4.test.helpers import setup_phase
from meinberlin.apps.budgeting.phases import VotingPhase

component = components.modules.get('voting_token_generation')


@patch('meinberlin.apps.votes.tasks.BATCH_SIZE', 10)
@pytest.mark.django_db
def test_token_generate_view(client, phase_factory, module_factory,
                             voting_token_factory, admin):
    phase, module, project, item = setup_phase(
        phase_factory, None, VotingPhase)
    other_module = module_factory()
    voting_token_factory(module=module)
    voting_token_factory(module=module)
    voting_token_factory(module=module, is_active=False)
    voting_token_factory(module=other_module)

    # initiator cannot access token generation view
    initiator = module.project.organisation.initiators.first()
    url = component.get_base_url(module)
    client.login(username=initiator.email, password='password')
    response = client.get(url)
    assert response.status_code == 403
    # admin can access view and generate tokens
    client.login(username=admin.email, password='password')
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
    messages = list(get_messages(response.wsgi_request))
    assert len(messages) == 1
    assert str(messages[0]) == (
        '12 codes will be generated in the background. Please come back '
        'later to check if they are finished')
    assert Task.objects.all().count() == 2
    task_1 = Task.objects.first()
    task_2 = Task.objects.last()
    assert task_1.task_name == \
        'meinberlin.apps.votes.tasks.generate_voting_tokens_batch'
    assert task_1.task_params == '[[' + str(module.id) + ', 10], {}]'
    assert task_2.task_params == '[[' + str(module.id) + ', 2], {}]'


@patch('meinberlin.apps.votes.views.TOKENS_PER_MODULE', 5)
@pytest.mark.django_db
def test_token_generate_view_max_validation(
        client, phase_factory, voting_token_factory, rf, admin):
    phase, module, project, item = setup_phase(
        phase_factory, None, VotingPhase)
    voting_token_factory(module=module)
    voting_token_factory(module=module)

    url = component.get_base_url(module)
    client.login(username=admin.email, password='password')
    data = {
        'number_of_tokens': 5
    }

    with translation.override('en_GB'):
        response = client.post(url, data)
    assert redirect_target(response) == 'voting-token-generation'
    messages = list(get_messages(response.wsgi_request))
    assert len(messages) == 1
    assert str(messages[0]) == (
        'Only 5 tokens are allowed per module. You are allowed to '
        'generate 3 more.')
    assert Task.objects.all().count() == 0

import pytest
from django.urls import reverse
from django.utils import translation

from adhocracy4.test.helpers import freeze_phase
from adhocracy4.test.helpers import setup_phase
from meinberlin.apps.budgeting import phases
from tests.votes.test_token_vote_api import add_token_to_session


@pytest.mark.django_db
def test_proposal_list_mixins(apiclient, phase_factory, proposal_factory,
                              voting_token_factory):
    phase, module, project, proposal = setup_phase(phase_factory,
                                                   proposal_factory,
                                                   phases.SupportPhase)
    token = voting_token_factory(module=module)
    add_token_to_session(apiclient, token)

    url = reverse('proposals-list',
                  kwargs={'module_pk': module.pk})

    response = apiclient.get(url)

    # locale info
    assert 'locale' in response.data
    assert response.data['locale'] == translation.get_language()

    # token info
    assert 'token_info' in response.data
    assert response.data['token_info']['votes_left']
    assert response.data['token_info']['num_votes_left'] == 5

    # permission info
    assert 'permissions' in response.data
    assert not response.data['permissions']['view_support_count']
    assert not response.data['permissions']['view_rate_count']
    assert not response.data['permissions']['view_comment_count']

    with freeze_phase(phase):
        response = apiclient.get(url)
        assert response.data['permissions']['view_support_count']
        assert not response.data['permissions']['view_rate_count']
        assert not response.data['permissions']['view_comment_count']

    phase_factory(phase_content=phases.CollectPhase(), module=module)
    phase_factory(phase_content=phases.RatingPhase(), module=module)
    response = apiclient.get(url)
    assert not response.data['permissions']['view_support_count']
    assert response.data['permissions']['view_rate_count']
    assert response.data['permissions']['view_comment_count']

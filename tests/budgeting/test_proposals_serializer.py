import pytest
from django.urls import reverse

from adhocracy4.test.helpers import freeze_phase
from meinberlin.apps.budgeting import phases
from tests.votes.test_token_vote_api import add_token_to_session


@pytest.mark.django_db
def test_proposal_serializer(apiclient, module, proposal_factory,
                             rating_factory, comment_factory, phase_factory,
                             token_vote_factory, voting_token_factory):

    url = reverse('proposals-list',
                  kwargs={'module_pk': module.pk})
    token = voting_token_factory(module=module)
    add_token_to_session(apiclient, token)

    proposal_rated = proposal_factory(module=module)
    rating_factory(content_object=proposal_rated)

    proposal_commented = proposal_factory(module=module)
    comment_factory(content_object=proposal_commented)

    proposal_voted = proposal_factory(module=module)
    token_vote_factory(token=token, content_object=proposal_voted)

    response = apiclient.get(url)
    proposal_data = response.data['results']
    assert len(proposal_data) == 3

    proposal_rated_data = [p for p in proposal_data if p['pk'] ==
                           proposal_rated.pk][0]
    proposal_commented_data = [p for p in proposal_data if p['pk'] ==
                               proposal_commented.pk][0]
    proposal_voted_data = [p for p in proposal_data if p['pk'] ==
                           proposal_voted.pk][0]

    assert proposal_rated_data['negative_rating_count'] == 0
    assert proposal_rated_data['positive_rating_count'] == 1
    assert proposal_rated_data['comment_count'] == 0
    assert not proposal_rated_data['vote_allowed']
    assert not proposal_rated_data['session_token_voted']

    assert proposal_commented_data['negative_rating_count'] == 0
    assert proposal_commented_data['positive_rating_count'] == 0
    assert proposal_commented_data['comment_count'] == 1
    assert not proposal_commented_data['vote_allowed']
    assert not proposal_commented_data['session_token_voted']

    assert proposal_voted_data['negative_rating_count'] == 0
    assert proposal_voted_data['positive_rating_count'] == 0
    assert proposal_voted_data['comment_count'] == 0
    assert not proposal_voted_data['vote_allowed']
    assert proposal_voted_data['session_token_voted']

    # test that vote allowed is only true for 3 phase budgeting
    voting_phase = phase_factory(phase_content=phases.VotingPhase(),
                                 module=module)

    with freeze_phase(voting_phase):
        response = apiclient.get(url)

    proposal_data = response.data['results']
    proposal_rated_data = [p for p in proposal_data if p['pk'] ==
                           proposal_rated.pk][0]
    proposal_commented_data = [p for p in proposal_data if p['pk'] ==
                               proposal_commented.pk][0]
    proposal_voted_data = [p for p in proposal_data if p['pk'] ==
                           proposal_voted.pk][0]

    assert not proposal_rated_data['vote_allowed']
    assert not proposal_commented_data['vote_allowed']
    assert not proposal_voted_data['vote_allowed']

    phase_factory(phase_content=phases.CollectPhase(), module=module)
    phase_factory(phase_content=phases.RatingPhase(), module=module)

    with freeze_phase(voting_phase):
        response = apiclient.get(url)

    proposal_data = response.data['results']
    proposal_rated_data = [p for p in proposal_data if p['pk'] ==
                           proposal_rated.pk][0]
    proposal_commented_data = [p for p in proposal_data if p['pk'] ==
                               proposal_commented.pk][0]
    proposal_voted_data = [p for p in proposal_data if p['pk'] ==
                           proposal_voted.pk][0]

    assert proposal_rated_data['vote_allowed']
    assert proposal_commented_data['vote_allowed']
    assert proposal_voted_data['vote_allowed']

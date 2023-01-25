import pytest
from django.urls import reverse

from adhocracy4.test.helpers import freeze_phase
from meinberlin.apps.budgeting import phases
from tests.votes.test_token_vote_api import add_token_to_session


@pytest.mark.django_db
def test_proposal_serializer(
    apiclient,
    module,
    proposal_factory,
    rating_factory,
    comment_factory,
    phase_factory,
    token_vote_factory,
    voting_token_factory,
    category_factory,
    label_factory,
):

    category = category_factory(module=module)
    label = label_factory(module=module)

    url = reverse("proposals-list", kwargs={"module_pk": module.pk})
    token = voting_token_factory(module=module)
    add_token_to_session(apiclient.session, token)

    proposal_rated = proposal_factory(
        module=module, category=category, budget=25, point_label=""
    )
    rating_factory(content_object=proposal_rated)
    proposal_rated.labels.set([label])

    proposal_commented = proposal_factory(module=module, category=category, budget=20)
    comment_factory(content_object=proposal_commented)

    proposal_voted = proposal_factory(module=module, budget=25, point_label="")
    proposal_voted.labels.set([label])
    token_vote_factory(token=token, content_object=proposal_voted)

    response = apiclient.get(url)
    proposal_data = response.data["results"]
    assert len(proposal_data) == 3

    proposal_rated_data = [p for p in proposal_data if p["pk"] == proposal_rated.pk][0]
    proposal_commented_data = [
        p for p in proposal_data if p["pk"] == proposal_commented.pk
    ][0]
    proposal_voted_data = [p for p in proposal_data if p["pk"] == proposal_voted.pk][0]

    assert proposal_rated_data["additional_item_badges_for_list_count"] == 1
    assert proposal_rated_data["comment_count"] == 0
    assert proposal_rated_data["creator"] == proposal_rated.creator.username
    assert proposal_rated_data["is_archived"] == proposal_rated.is_archived
    assert proposal_rated_data["item_badges_for_list"] == [
        [
            "moderator_status",
            proposal_rated.get_moderator_status_display(),
            proposal_rated.moderator_status,
        ],
        ["budget", "{}€".format(proposal_rated.budget)],
        ["category", proposal_rated.category.name],
    ]
    assert proposal_rated_data["name"] == proposal_rated.name
    assert proposal_rated_data["negative_rating_count"] == 0
    assert proposal_rated_data["pk"] == proposal_rated.pk
    assert proposal_rated_data["positive_rating_count"] == 1
    assert proposal_rated_data["reference_number"] == proposal_rated.reference_number
    assert not proposal_rated_data["session_token_voted"]
    assert proposal_rated_data["url"] == proposal_rated.get_absolute_url()
    assert not proposal_rated_data["vote_allowed"]

    assert proposal_commented_data["additional_item_badges_for_list_count"] == 1
    assert proposal_commented_data["comment_count"] == 1
    assert proposal_commented_data["item_badges_for_list"] == [
        [
            "moderator_status",
            proposal_commented.get_moderator_status_display(),
            proposal_commented.moderator_status,
        ],
        ["budget", "{}€".format(proposal_commented.budget)],
        ["point_label", proposal_commented.point_label],
    ]
    assert proposal_commented_data["negative_rating_count"] == 0
    assert proposal_commented_data["positive_rating_count"] == 0
    assert not proposal_commented_data["session_token_voted"]
    assert not proposal_commented_data["vote_allowed"]

    assert proposal_voted_data["additional_item_badges_for_list_count"] == 0
    assert proposal_voted_data["comment_count"] == 0
    assert proposal_voted_data["item_badges_for_list"] == [
        [
            "moderator_status",
            proposal_voted.get_moderator_status_display(),
            proposal_voted.moderator_status,
        ],
        ["budget", "{}€".format(proposal_voted.budget)],
        ["label", label.name],
    ]
    assert proposal_voted_data["negative_rating_count"] == 0
    assert proposal_voted_data["positive_rating_count"] == 0
    assert proposal_voted_data["session_token_voted"]
    assert not proposal_voted_data["vote_allowed"]

    # test that vote allowed is only true for 3 phase budgeting
    voting_phase = phase_factory(phase_content=phases.VotingPhase(), module=module)

    with freeze_phase(voting_phase):
        response = apiclient.get(url)

    proposal_data = response.data["results"]
    proposal_rated_data = [p for p in proposal_data if p["pk"] == proposal_rated.pk][0]
    proposal_commented_data = [
        p for p in proposal_data if p["pk"] == proposal_commented.pk
    ][0]
    proposal_voted_data = [p for p in proposal_data if p["pk"] == proposal_voted.pk][0]

    assert not proposal_rated_data["vote_allowed"]
    assert not proposal_commented_data["vote_allowed"]
    assert not proposal_voted_data["vote_allowed"]

    module.blueprint_type = "PB3"
    module.save()

    with freeze_phase(voting_phase):
        response = apiclient.get(url)

    proposal_data = response.data["results"]
    proposal_rated_data = [p for p in proposal_data if p["pk"] == proposal_rated.pk][0]
    proposal_commented_data = [
        p for p in proposal_data if p["pk"] == proposal_commented.pk
    ][0]
    proposal_voted_data = [p for p in proposal_data if p["pk"] == proposal_voted.pk][0]

    assert proposal_rated_data["vote_allowed"]
    assert proposal_commented_data["vote_allowed"]
    assert proposal_voted_data["vote_allowed"]

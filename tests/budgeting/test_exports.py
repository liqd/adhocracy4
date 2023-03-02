import pytest
from django.urls import reverse

from adhocracy4.ratings.models import Rating
from meinberlin.apps.budgeting.exports import ItemExportWithSupportMixin
from meinberlin.apps.budgeting.exports import ItemExportWithTokenVotesMixin
from meinberlin.apps.budgeting.models import Proposal


@pytest.mark.django_db
def test_proposal_export_view(client, proposal_factory, user):
    proposal = proposal_factory()
    organisation = proposal.module.project.organisation
    initiator = organisation.initiators.first()
    url = reverse(
        "a4dashboard:budgeting-export", kwargs={"module_slug": proposal.module.slug}
    )
    client.login(username=user.email, password="password")
    response = client.get(url)
    assert response.status_code == 403
    client.login(username=initiator.email, password="password")
    response = client.get(url)
    assert response.status_code == 200
    assert (
        response["Content-Type"] == "application/vnd.openxmlformats-officedocument."
        "spreadsheetml.sheet"
    )


@pytest.mark.django_db
def test_proposal_comment_export_view(client, proposal_factory, user):
    proposal = proposal_factory()
    organisation = proposal.module.project.organisation
    initiator = organisation.initiators.first()
    url = reverse(
        "a4dashboard:budgeting-comment-export",
        kwargs={"module_slug": proposal.module.slug},
    )
    client.login(username=user.email, password="password")
    response = client.get(url)
    assert response.status_code == 403
    client.login(username=initiator.email, password="password")
    response = client.get(url)
    assert response.status_code == 200
    assert (
        response["Content-Type"] == "application/vnd.openxmlformats-officedocument."
        "spreadsheetml.sheet"
    )


@pytest.mark.django_db
def test_pb3_proposal_export_view(client, proposal_factory, user):
    proposal = proposal_factory()
    organisation = proposal.module.project.organisation
    initiator = organisation.initiators.first()
    url = reverse(
        "a4dashboard:3-phase-budgeting-export",
        kwargs={"module_slug": proposal.module.slug},
    )
    client.login(username=user.email, password="password")
    response = client.get(url)
    assert response.status_code == 403
    client.login(username=initiator.email, password="password")
    response = client.get(url)
    assert response.status_code == 200
    assert (
        response["Content-Type"] == "application/vnd.openxmlformats-officedocument."
        "spreadsheetml.sheet"
    )


@pytest.mark.django_db
def test_item_support_mixin(module, proposal_factory, rating_factory):
    proposal_1 = proposal_factory(module=module)
    proposal_2 = proposal_factory(module=module)
    rating_factory(content_object=proposal_1, value=Rating.POSITIVE)
    rating_factory(content_object=proposal_1, value=Rating.POSITIVE)

    mixin = ItemExportWithSupportMixin()

    virtual = mixin.get_virtual_fields({})
    assert "support" in virtual

    # Test explicit counting
    assert mixin.get_support_data(proposal_1) == 2
    assert mixin.get_support_data(proposal_2) == 0

    # Test annotated counting
    proposal = Proposal.objects.annotate_positive_rating_count().first()
    assert mixin.get_support_data(proposal) == 2


@pytest.mark.django_db
def test_item_token_votes_mixin(
    module,
    proposal_factory,
    token_vote_factory,
    voting_token_factory,
):
    proposal_1 = proposal_factory(module=module)
    proposal_2 = proposal_factory(module=module)
    token = voting_token_factory(module=module)
    token_vote_factory(token=token, content_object=proposal_1)

    mixin = ItemExportWithTokenVotesMixin()

    virtual = mixin.get_virtual_fields({})
    assert "token_vote_count" in virtual

    # Test without annotations -> do we need explicit counting?
    assert mixin.get_token_vote_count_data(proposal_1) == 0
    assert mixin.get_token_vote_count_data(proposal_2) == 0

    # Test annotated counting
    annotated_proposals = Proposal.objects.annotate_token_vote_count()
    assert mixin.get_token_vote_count_data(annotated_proposals.first()) == 1
    assert mixin.get_token_vote_count_data(annotated_proposals.last()) == 0

import html
import json
import re
from unittest.mock import Mock

import pytest
from django.contrib.contenttypes.models import ContentType
from django.contrib.sessions.middleware import SessionMiddleware
from django.urls import reverse

from adhocracy4.test.helpers import freeze_phase
from adhocracy4.test.helpers import freeze_post_phase
from adhocracy4.test.helpers import render_template
from adhocracy4.test.helpers import setup_phase
from meinberlin.apps.budgeting import phases
from meinberlin.apps.budgeting.models import Proposal
from tests.votes.test_token_vote_api import add_token_to_session


@pytest.mark.django_db
def test_react_proposals(module, rf):
    request = rf.get("/")
    template = "{% load react_proposals %}{% react_proposals module %}"
    contenttype = ContentType.objects.get_for_model(Proposal)
    expected = (
        r"^<div data-mb-widget=\"proposals\" data-attributes="
        r"\"(?P<props>{.+})\"><\/div>$"
    )

    props = get_rendered_props(
        {"request": request, "module": module}, expected, template
    )
    assert props == {
        "proposals_api_url": reverse("proposals-list", kwargs={"module_pk": module.pk}),
        "tokenvote_api_url": reverse(
            "tokenvotes-list",
            kwargs={"module_pk": module.pk, "content_type": contenttype.id},
        ),
        "end_session_url": reverse("end_session"),
    }


@pytest.mark.django_db
def test_react_proposals_vote(
    phase_factory, proposal_factory, voting_token_factory, token_vote_factory, user, rf
):
    phase, module, project, proposal = setup_phase(
        phase_factory, proposal_factory, phases.VotingPhase
    )

    request = rf.get("/")
    middleware = SessionMiddleware(Mock())
    middleware.process_request(request)
    request.session.save()
    request.user = user

    template = (
        "{% load react_proposals_vote %}" "{% react_proposals_vote module proposal %}"
    )
    contenttype = ContentType.objects.get_for_model(Proposal)
    expected = (
        r"^<div data-mb-widget=\"vote_button\" data-attributes="
        r"\"(?P<props>{.+})\"><\/div>$"
    )

    with freeze_phase(phase):
        proposal = get_annotated_proposal(module)
        props = get_rendered_props(
            {"request": request, "module": module, "proposal": proposal},
            expected,
            template,
        )
        assert props == {
            "tokenvote_api_url": reverse(
                "tokenvotes-list",
                kwargs={"module_pk": module.pk, "content_type": contenttype.id},
            ),
            "objectID": proposal.pk,
            "session_token_voted": False,
            "token_info": None,
        }

    token = voting_token_factory(module=module)
    add_token_to_session(request.session, token)
    token_vote_factory(token=token, content_object=proposal)

    with freeze_phase(phase):
        proposal = get_annotated_proposal(module)
        props = get_rendered_props(
            {"request": request, "module": module, "proposal": proposal},
            expected,
            template,
        )
        assert props == {
            "tokenvote_api_url": reverse(
                "tokenvotes-list",
                kwargs={"module_pk": module.pk, "content_type": contenttype.id},
            ),
            "objectID": proposal.pk,
            "session_token_voted": True,
            "token_info": {
                "votes_left": True,
                "num_votes_left": token.allowed_votes - 1,
            },
        }


@pytest.mark.django_db
def test_react_support(phase_factory, proposal_factory, rating_factory, user, rf):
    phase, module, project, proposal = setup_phase(
        phase_factory, proposal_factory, phases.SupportPhase
    )

    request = rf.get("/")
    request.user = user
    template = "{% load react_support %}{% react_support proposal %}"
    contenttype = ContentType.objects.get_for_model(Proposal)
    expected = (
        r"^<div data-mb-widget=\"support\" data-attributes="
        r"\"(?P<props>{.+})\"><\/div>$"
    )

    with freeze_phase(phase):
        proposal = get_annotated_proposal(module)
        props = get_rendered_props(
            {"request": request, "proposal": proposal}, expected, template
        )
        assert props == {
            "contentType": contenttype.id,
            "objectId": proposal.pk,
            "authenticated": True,
            "support": 0,
            "userSupported": False,
            "userSupportId": -1,
            "isReadOnly": False,
            "isArchived": False,
        }

    rating = rating_factory(content_object=proposal, creator=user)

    with freeze_post_phase(phase):
        proposal = get_annotated_proposal(module)
        props = get_rendered_props(
            {"request": request, "proposal": proposal}, expected, template
        )
        assert props == {
            "contentType": contenttype.id,
            "objectId": proposal.pk,
            "authenticated": True,
            "support": 1,
            "userSupported": True,
            "userSupportId": rating.pk,
            "isReadOnly": True,
            "isArchived": False,
        }


def get_annotated_proposal(module):
    qs = Proposal.objects.filter(module=module)
    annotated_qs = qs.annotate_positive_rating_count().annotate_negative_rating_count()
    proposal = annotated_qs.first()
    return proposal


def get_rendered_props(context, expected, template):
    rendered_template = render_template(template, context)
    match = re.match(expected, rendered_template)
    props = json.loads(html.unescape(match.group("props")))
    return props

from datetime import timedelta

import pytest
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from rest_framework import status

from adhocracy4.test.helpers import freeze_time
from adhocracy4.test.helpers import setup_phase
from meinberlin.apps.budgeting import phases
from meinberlin.apps.budgeting.views import TOKEN_SESSION_EXPIRE
from meinberlin.apps.votes.models import TokenVote


@pytest.mark.django_db
def test_token_deleted_from_session(
    apiclient, voting_token_factory, phase_factory, proposal_factory
):
    phase, module, project, proposal = setup_phase(
        phase_factory, proposal_factory, phases.VotingPhase
    )
    proposal_ct = ContentType.objects.get_for_model(proposal.__class__)
    token = voting_token_factory(module=module)

    url_project = project.get_absolute_url()

    url_post = reverse(
        "tokenvotes-list",
        kwargs={"module_pk": module.pk, "content_type": proposal_ct.id},
    )
    url_delete = reverse(
        "tokenvotes-detail",
        kwargs={
            "module_pk": module.pk,
            "content_type": proposal_ct.id,
            "object_pk": proposal.pk,
        },
    )

    proposal_data = {"object_id": proposal.pk}
    token_data = {"token": str(token)}

    phase_started = phase.start_date + timedelta(seconds=1)

    with freeze_time(phase_started):
        # post token
        response = apiclient.post(url_project, token_data)
        assert response.status_code == 302

        # post and delete token vote
        response = apiclient.post(url_post, proposal_data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert TokenVote.objects.all().count() == 1
        response = apiclient.delete(url_delete, format="json")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert TokenVote.objects.all().count() == 0

        assert "voting_tokens" in apiclient.session
        assert "token_expire_date" in apiclient.session

    with freeze_time(phase_started + TOKEN_SESSION_EXPIRE):
        response = apiclient.post(url_post, proposal_data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert "voting_tokens" not in apiclient.session
        assert "token_expire_date" not in apiclient.session

        # post token again
        response = apiclient.post(url_project, token_data)
        assert response.status_code == 302

        response = apiclient.post(url_post, proposal_data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert "voting_tokens" in apiclient.session
        assert "token_expire_date" in apiclient.session


@pytest.mark.django_db
def test_token_expire_date_renewed(
    apiclient, voting_token_factory, phase_factory, proposal_factory, module_factory
):
    phase_1, module_1, project, _ = setup_phase(
        phase_factory, proposal_factory, phases.VotingPhase
    )
    module_2 = module_factory(project=project)
    phase_2 = phase_factory(
        phase_content=phases.VotingPhase(),
        module=module_2,
        start_date=phase_1.start_date + TOKEN_SESSION_EXPIRE * 0.5,
        end_date=phase_1.end_date + TOKEN_SESSION_EXPIRE * 0.5,
    )

    token_1 = voting_token_factory(module=module_1)
    token_2 = voting_token_factory(module=module_2)

    url_module_1 = module_1.get_absolute_url()
    url_module_2 = module_2.get_absolute_url()

    token_data_1 = {"token": str(token_1)}
    token_data_2 = {"token": str(token_2)}

    phase_1_started = phase_1.start_date + timedelta(seconds=1)
    phase_2_started = phase_2.start_date + timedelta(seconds=1)

    with freeze_time(phase_1_started):
        response = apiclient.post(url_module_1, token_data_1)
        assert response.status_code == 302

        assert "voting_tokens" in apiclient.session
        assert str(module_1.id) in apiclient.session["voting_tokens"]
        assert "token_expire_date" in apiclient.session
        assert (
            apiclient.session["token_expire_date"]
            == (phase_1_started + TOKEN_SESSION_EXPIRE).timestamp()
        )

    with freeze_time(phase_2_started):
        response = apiclient.post(url_module_2, token_data_2)
        assert response.status_code == 302

        assert "voting_tokens" in apiclient.session
        assert str(module_1.id) in apiclient.session["voting_tokens"]
        assert str(module_2.id) in apiclient.session["voting_tokens"]
        assert "token_expire_date" in apiclient.session
        assert (
            apiclient.session["token_expire_date"]
            == (phase_2_started + TOKEN_SESSION_EXPIRE).timestamp()
        )

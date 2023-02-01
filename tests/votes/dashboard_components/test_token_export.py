from unittest.mock import patch

import pytest
from django.urls import reverse

from adhocracy4.dashboard import components
from adhocracy4.test.helpers import dispatch_view
from adhocracy4.test.helpers import setup_phase
from meinberlin.apps.budgeting.phases import VotingPhase
from meinberlin.apps.votes.exports import TokenExportView

component = components.modules.get("voting_token_export")


@patch("meinberlin.apps.votes.views.PAGE_SIZE", 2)
@pytest.mark.django_db
def test_token_vote_view(client, phase_factory, module_factory, voting_token_factory):
    phase, module, project, item = setup_phase(phase_factory, None, VotingPhase)
    other_module = module_factory()
    voting_token_factory(module=module)
    voting_token_factory(module=module)
    voting_token_factory(module=module)
    voting_token_factory(module=module, is_active=False)
    voting_token_factory(module=other_module)

    initiator = module.project.organisation.initiators.first()
    url = component.get_base_url(module)
    client.login(username=initiator.email, password="password")
    response = client.get(url)
    assert response.status_code == 200
    assert "token_export_url" in response.context
    assert "token_export_iterator" in response.context
    assert "number_of_module_tokens" in response.context
    export_url = response.context["token_export_url"]
    token_export_iterator = response.context["token_export_iterator"]
    number_of_module_tokens = response.context["number_of_module_tokens"]

    response = client.get(export_url)
    assert response.status_code == 200
    assert (
        response.get("Content-Type")
        == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    assert token_export_iterator == range(1, 3)
    assert number_of_module_tokens == "3"


@pytest.mark.django_db
def test_export(voting_token, rf):
    module = voting_token.module
    initiator = module.project.organisation.initiators.first()
    token_export_url = reverse(
        "a4dashboard:token-export", kwargs={"module_slug": module.slug}
    )
    request = rf.get(token_export_url)
    request.user = initiator
    response, view = dispatch_view(TokenExportView, request, module=module)
    assert voting_token in view.get_queryset()
    assert module.project.slug in view.get_base_filename()
    assert view.get_token_data(voting_token) == str(voting_token)

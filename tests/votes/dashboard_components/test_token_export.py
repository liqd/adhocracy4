import pytest
from django.urls import reverse

from adhocracy4.dashboard import components
from adhocracy4.test.helpers import dispatch_view
from adhocracy4.test.helpers import setup_phase
from meinberlin.apps.budgeting.phases import VotingPhase
from meinberlin.apps.votes.exports import TokenExportView
from meinberlin.apps.votes.models import VotingToken

component = components.modules.get("voting_token_export")


@pytest.mark.django_db
def test_token_vote_view(client, phase_factory, module_factory, voting_token_factory):
    phase, module, project, item = setup_phase(phase_factory, None, VotingPhase)
    other_module = module_factory()
    voting_token_factory(module=module)
    voting_token_factory(module=module, package_number=1)
    voting_token_factory(module=module, package_number=2)
    voting_token_factory(module=module, package_number=3, is_active=False)
    voting_token_factory(module=other_module)

    initiator = module.project.organisation.initiators.first()
    url = component.get_base_url(module)
    client.login(username=initiator.email, password="password")
    response = client.get(url)
    assert response.status_code == 200
    assert "token_export_url" in response.context
    assert "token_packages" in response.context
    assert "number_of_module_tokens" in response.context
    export_url = response.context["token_export_url"]
    token_packages = response.context["token_packages"]
    number_of_module_tokens = response.context["number_of_module_tokens"]

    assert len(token_packages) == 3
    # assert packages are downloadable and have right package_number
    for count, package in enumerate(token_packages):
        assert package[0] == count
        assert package[1]

    response = client.get(export_url)
    assert response.status_code == 200
    assert (
        response.get("Content-Type")
        == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    assert number_of_module_tokens == "3"

    response = client.get(url)
    assert response.status_code == 200
    token_packages = response.context["token_packages"]
    assert len(token_packages) == 3
    # assert that first package is no longer downloadable
    for count, package in enumerate(token_packages):
        assert package[0] == count
        if count == 0:
            assert not package[1]
        else:
            assert package[1]


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
    voting_token = VotingToken.objects.get(id=voting_token.id)
    # token should no longer be in the queryset
    assert voting_token not in view.get_queryset()
    assert not voting_token.token
    assert module.project.slug in view.get_base_filename()
    assert view.get_token_data(voting_token) == str(voting_token)

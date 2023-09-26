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
def test_token_vote_view(
    client, phase_factory, module_factory, token_package_factory, voting_token_factory
):
    phase, module, project, item = setup_phase(phase_factory, None, VotingPhase)
    other_module = module_factory()
    package0 = token_package_factory(module=module)
    package1 = token_package_factory(module=module)
    package2 = token_package_factory(module=module)
    package3 = token_package_factory(module=module)
    voting_token_factory(module=module, package=package0)
    voting_token_factory(module=module, package=package1)
    voting_token_factory(module=module, package=package2)
    voting_token_factory(module=module, package=package3, is_active=False)
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

    assert len(token_packages) == 4
    # assert packages are downloadable and have right package_number and size
    packages = [package0, package1, package2, package3]
    for count, package in enumerate(token_packages):
        assert package[0] == packages[count].pk
        assert package[1] is False
        assert package[2] == 1

    response = client.get(export_url + "?package=" + str(package0.pk))
    assert response.status_code == 200
    assert (
        response.get("Content-Type")
        == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    assert number_of_module_tokens == "4"

    response = client.get(url)
    assert response.status_code == 200
    token_packages = response.context["token_packages"]
    assert len(token_packages) == 4


@pytest.mark.django_db
def test_export(voting_token, rf):
    module = voting_token.module
    initiator = module.project.organisation.initiators.first()
    token_export_url = reverse(
        "a4dashboard:token-export", kwargs={"module_slug": module.slug}
    )
    request = rf.get(token_export_url + "?package=" + str(voting_token.package.pk))
    request.user = initiator
    response, view = dispatch_view(TokenExportView, request, module=module)
    voting_token = VotingToken.objects.get(id=voting_token.id)
    assert module.project.slug in view.get_base_filename()
    assert view.get_token_data(voting_token) == str(voting_token)

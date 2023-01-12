import pytest
from django.urls import reverse

from adhocracy4.dashboard import components
from adhocracy4.polls.phases import VotingPhase
from adhocracy4.test.helpers import assert_template_response
from adhocracy4.test.helpers import redirect_target
from adhocracy4.test.helpers import setup_phase

poll_component = components.modules.get("polls")
export_poll_component = components.modules.get("poll_export")


@pytest.mark.django_db
def test_poll_edit_view(client, phase_factory, user_factory):
    phase, module, project, item = setup_phase(phase_factory, None, VotingPhase)
    initiator = user_factory()
    project.organisation.initiators.add(initiator)
    url = poll_component.get_base_url(module)
    client.login(username=initiator.username, password="password")
    response = client.get(url)
    assert_template_response(response, "a4polls/poll_dashboard.html")
    assert response.template_name[0] == "a4polls/poll_dashboard.html"


@pytest.mark.django_db
def test_poll_dashboard_export_view(client, phase_factory, user_factory):
    phase, module, project, item = setup_phase(phase_factory, None, VotingPhase)
    user = user_factory()
    initiator = user_factory()
    project.organisation.initiators.add(initiator)
    url = export_poll_component.get_base_url(module)

    client.login(username=user.username, password="password")
    response = client.get(url)
    assert response.status_code == 403

    client.login(username=initiator.username, password="password")
    response = client.get(url)
    assert_template_response(response, "a4exports/export_dashboard.html")
    assert response.template_name[0] == "a4exports/export_dashboard.html"
    assert "poll_export" in response.context
    assert response.context["poll_export"] == reverse(
        "a4dashboard:poll-export", kwargs={"module_slug": module.slug}
    )
    assert "comment_export" in response.context
    assert response.context["comment_export"] == reverse(
        "a4dashboard:poll-comment-export", kwargs={"module_slug": module.slug}
    )


@pytest.mark.django_db
def test_poll_export_view(
    client, phase_factory, user_factory, group_factory, poll_factory
):

    phase, module, project, item = setup_phase(phase_factory, poll_factory, VotingPhase)

    user = user_factory()
    moderator = user_factory()
    project.moderators.add(moderator)

    initiator = user_factory()
    project.organisation.initiators.add(initiator)

    group = group_factory()
    group_member = user_factory.create(groups=[group])
    project.group = group
    project.save()

    url = reverse("a4dashboard:poll-export", kwargs={"module_slug": module.slug})

    response = client.get(url)
    assert redirect_target(response) == "account_login"

    client.login(username=user, password="password")
    response = client.get(url)
    assert response.status_code == 403

    client.login(username=moderator, password="password")
    response = client.get(url)
    assert response.status_code == 403

    client.login(username=initiator, password="password")
    response = client.get(url)
    assert response.status_code == 200

    client.login(username=group_member, password="password")
    response = client.get(url)
    assert response.status_code == 200
    assert (
        response["Content-Type"]
        == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    assert project.slug in response["Content-Disposition"]


@pytest.mark.django_db
def test_poll_comment_export_view(
    client, phase_factory, user_factory, group_factory, poll_factory
):

    phase, module, project, item = setup_phase(phase_factory, poll_factory, VotingPhase)

    user = user_factory()
    moderator = user_factory()
    project.moderators.add(moderator)

    initiator = user_factory()
    project.organisation.initiators.add(initiator)

    group = group_factory()
    group_member = user_factory.create(groups=[group])
    project.group = group
    project.save()

    url = reverse(
        "a4dashboard:poll-comment-export", kwargs={"module_slug": module.slug}
    )

    response = client.get(url)
    assert redirect_target(response) == "account_login"

    client.login(username=user, password="password")
    response = client.get(url)
    assert response.status_code == 403

    client.login(username=moderator, password="password")
    response = client.get(url)
    assert response.status_code == 403

    client.login(username=initiator, password="password")
    response = client.get(url)
    assert response.status_code == 200

    client.login(username=group_member, password="password")
    response = client.get(url)
    assert response.status_code == 200
    assert (
        response["Content-Type"]
        == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    assert project.slug in response["Content-Disposition"]

import pytest
from django.urls import reverse

from adhocracy4.test.helpers import assert_template_response
from adhocracy4.test.helpers import freeze_phase
from adhocracy4.test.helpers import redirect_target
from adhocracy4.test.helpers import setup_phase
from meinberlin.apps.ideas import models
from meinberlin.apps.ideas import phases


@pytest.mark.django_db
def test_anonymous_cannot_delete(client, idea_factory):
    idea = idea_factory()
    url = reverse(
        "meinberlin_ideas:idea-delete",
        kwargs={"pk": idea.pk, "year": idea.created.year},
    )
    response = client.get(url)
    assert response.status_code == 302
    assert redirect_target(response) == "account_login"


@pytest.mark.django_db
def test_user_cannot_delete(client, idea_factory, user):
    idea = idea_factory()
    client.login(username=user.email, password="password")
    url = reverse(
        "meinberlin_ideas:idea-delete",
        kwargs={"pk": idea.pk, "year": idea.created.year},
    )
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_creator_cannot_delete(client, idea_factory):
    idea = idea_factory()
    client.login(username=idea.creator.email, password="password")
    url = reverse(
        "meinberlin_ideas:idea-delete",
        kwargs={"pk": idea.pk, "year": idea.created.year},
    )
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_moderator_can_delete(client, idea_factory):
    idea = idea_factory()
    moderator = idea.module.project.moderators.first()
    client.login(username=moderator.email, password="password")
    url = reverse(
        "meinberlin_ideas:idea-delete",
        kwargs={"pk": idea.pk, "year": idea.created.year},
    )
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_initator_can_delete(client, idea_factory):
    idea = idea_factory()
    initiator = idea.module.project.organisation.initiators.first()
    client.login(username=initiator.email, password="password")
    url = reverse(
        "meinberlin_ideas:idea-delete",
        kwargs={"pk": idea.pk, "year": idea.created.year},
    )
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_admin_can_delete(client, idea_factory, admin):
    idea = idea_factory()
    client.login(username=admin.email, password="password")
    url = reverse(
        "meinberlin_ideas:idea-delete",
        kwargs={"pk": idea.pk, "year": idea.created.year},
    )
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_creator_can_delete_in_active_phase(client, phase_factory, idea_factory):
    phase, module, project, idea = setup_phase(
        phase_factory, idea_factory, phases.IssuePhase
    )
    url = reverse(
        "meinberlin_ideas:idea-delete",
        kwargs={"pk": idea.pk, "year": idea.created.year},
    )
    with freeze_phase(phase):
        count = models.Idea.objects.all().count()
        assert count == 1
        client.login(username=idea.creator.email, password="password")
        response = client.get(url)
        assert_template_response(response, "meinberlin_ideas/idea_confirm_delete.html")
        response = client.post(url)
        assert redirect_target(response) == "project-detail"
        assert response.status_code == 302
        count = models.Idea.objects.all().count()
        assert count == 0


@pytest.mark.django_db
def test_creator_cannot_delete_in_wrong_phase(client, phase_factory, idea_factory):

    phase, module, project, idea = setup_phase(
        phase_factory, idea_factory, phases.RatingPhase
    )
    url = reverse(
        "meinberlin_ideas:idea-delete",
        kwargs={"pk": idea.pk, "year": idea.created.year},
    )
    with freeze_phase(phase):
        count = models.Idea.objects.all().count()
        assert count == 1
        client.login(username=idea.creator.email, password="password")
        response = client.get(url)
        assert response.status_code == 403


@pytest.mark.django_db
def test_moderator_can_delete_in_active_phase(client, phase_factory, idea_factory):
    phase, module, project, idea = setup_phase(
        phase_factory, idea_factory, phases.IssuePhase
    )
    url = reverse(
        "meinberlin_ideas:idea-delete",
        kwargs={"pk": idea.pk, "year": idea.created.year},
    )
    with freeze_phase(phase):
        count = models.Idea.objects.all().count()
        assert count == 1
        moderator = idea.module.project.moderators.first()
        client.login(username=moderator.email, password="password")
        response = client.get(url)
        assert_template_response(response, "meinberlin_ideas/idea_confirm_delete.html")
        response = client.post(url)
        assert redirect_target(response) == "project-detail"
        assert response.status_code == 302
        count = models.Idea.objects.all().count()
        assert count == 0


@pytest.mark.django_db
def test_moderator_can_delete_in_wrong_phase(client, phase_factory, idea_factory):
    phase, module, project, idea = setup_phase(
        phase_factory, idea_factory, phases.RatingPhase
    )
    url = reverse(
        "meinberlin_ideas:idea-delete",
        kwargs={"pk": idea.pk, "year": idea.created.year},
    )
    with freeze_phase(phase):
        count = models.Idea.objects.all().count()
        assert count == 1
        moderator = idea.module.project.moderators.first()
        client.login(username=moderator.email, password="password")
        response = client.get(url)
        assert_template_response(response, "meinberlin_ideas/idea_confirm_delete.html")
        response = client.post(url)
        assert redirect_target(response) == "project-detail"
        assert response.status_code == 302
        count = models.Idea.objects.all().count()
        assert count == 0

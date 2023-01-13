import pytest
from django.urls import reverse

from adhocracy4.test.helpers import assert_template_response
from adhocracy4.test.helpers import freeze_phase
from adhocracy4.test.helpers import redirect_target
from adhocracy4.test.helpers import setup_phase
from meinberlin.apps.mapideas import models
from meinberlin.apps.mapideas import phases


@pytest.mark.django_db
def test_anonymous_cannot_delete(client, map_idea_factory):
    mapidea = map_idea_factory()
    url = reverse(
        "meinberlin_mapideas:mapidea-delete",
        kwargs={"pk": mapidea.pk, "year": mapidea.created.year},
    )
    response = client.get(url)
    assert response.status_code == 302
    assert redirect_target(response) == "account_login"


@pytest.mark.django_db
def test_user_cannot_delete(client, map_idea_factory, user):
    mapidea = map_idea_factory()
    client.login(username=user.email, password="password")
    url = reverse(
        "meinberlin_mapideas:mapidea-delete",
        kwargs={"pk": mapidea.pk, "year": mapidea.created.year},
    )
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_creator_cannot_delete(client, map_idea_factory):
    mapidea = map_idea_factory()
    client.login(username=mapidea.creator.email, password="password")
    url = reverse(
        "meinberlin_mapideas:mapidea-delete",
        kwargs={"pk": mapidea.pk, "year": mapidea.created.year},
    )
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_moderator_can_delete(client, map_idea_factory):
    mapidea = map_idea_factory()
    moderator = mapidea.module.project.moderators.first()
    client.login(username=moderator.email, password="password")
    url = reverse(
        "meinberlin_mapideas:mapidea-delete",
        kwargs={"pk": mapidea.pk, "year": mapidea.created.year},
    )
    response = client.get(url)
    assert_template_response(
        response, "meinberlin_mapideas/mapidea_confirm_delete.html"
    )


@pytest.mark.django_db
def test_initator_can_delete(client, map_idea_factory):
    mapidea = map_idea_factory()
    initiator = mapidea.module.project.organisation.initiators.first()
    client.login(username=initiator.email, password="password")
    url = reverse(
        "meinberlin_mapideas:mapidea-delete",
        kwargs={"pk": mapidea.pk, "year": mapidea.created.year},
    )
    response = client.get(url)
    assert_template_response(
        response, "meinberlin_mapideas/mapidea_confirm_delete.html"
    )


@pytest.mark.django_db
def test_admin_can_delete(client, map_idea_factory, admin):
    mapidea = map_idea_factory()
    client.login(username=admin.email, password="password")
    url = reverse(
        "meinberlin_mapideas:mapidea-delete",
        kwargs={"pk": mapidea.pk, "year": mapidea.created.year},
    )
    response = client.get(url)
    assert_template_response(
        response, "meinberlin_mapideas/mapidea_confirm_delete.html"
    )


@pytest.mark.django_db
def test_creator_can_delete_in_active_phase(client, phase_factory, map_idea_factory):
    phase, module, project, mapidea = setup_phase(
        phase_factory, map_idea_factory, phases.IssuePhase
    )
    url = reverse(
        "meinberlin_mapideas:mapidea-delete",
        kwargs={"pk": mapidea.pk, "year": mapidea.created.year},
    )
    with freeze_phase(phase):
        count = models.MapIdea.objects.all().count()
        assert count == 1
        client.login(username=mapidea.creator.email, password="password")
        response = client.get(url)
        assert_template_response(
            response, "meinberlin_mapideas/mapidea_confirm_delete.html"
        )
        response = client.post(url)
        assert redirect_target(response) == "project-detail"
        assert response.status_code == 302
        count = models.MapIdea.objects.all().count()
        assert count == 0


@pytest.mark.django_db
def test_creator_cannot_delete_in_wrong_phase(client, phase_factory, map_idea_factory):

    phase, module, project, mapidea = setup_phase(
        phase_factory, map_idea_factory, phases.RatingPhase
    )
    url = reverse(
        "meinberlin_mapideas:mapidea-delete",
        kwargs={"pk": mapidea.pk, "year": mapidea.created.year},
    )
    with freeze_phase(phase):
        count = models.MapIdea.objects.all().count()
        assert count == 1
        client.login(username=mapidea.creator.email, password="password")
        response = client.get(url)
        assert response.status_code == 403


@pytest.mark.django_db
def test_moderator_can_delete_in_active_phase(client, phase_factory, map_idea_factory):
    phase, module, project, mapidea = setup_phase(
        phase_factory, map_idea_factory, phases.IssuePhase
    )
    url = reverse(
        "meinberlin_mapideas:mapidea-delete",
        kwargs={"pk": mapidea.pk, "year": mapidea.created.year},
    )
    with freeze_phase(phase):
        count = models.MapIdea.objects.all().count()
        assert count == 1
        moderator = mapidea.module.project.moderators.first()
        client.login(username=moderator.email, password="password")
        response = client.get(url)
        assert_template_response(
            response, "meinberlin_mapideas/mapidea_confirm_delete.html"
        )
        response = client.post(url)
        assert redirect_target(response) == "project-detail"
        assert response.status_code == 302
        count = models.MapIdea.objects.all().count()
        assert count == 0


@pytest.mark.django_db
def test_moderator_can_delete_in_wrong_phase(client, phase_factory, map_idea_factory):
    phase, module, project, mapidea = setup_phase(
        phase_factory, map_idea_factory, phases.RatingPhase
    )
    url = reverse(
        "meinberlin_mapideas:mapidea-delete",
        kwargs={"pk": mapidea.pk, "year": mapidea.created.year},
    )
    with freeze_phase(phase):
        count = models.MapIdea.objects.all().count()
        assert count == 1
        moderator = mapidea.module.project.moderators.first()
        client.login(username=moderator.email, password="password")
        response = client.get(url)
        assert_template_response(
            response, "meinberlin_mapideas/mapidea_confirm_delete.html"
        )
        response = client.post(url)
        assert redirect_target(response) == "project-detail"
        assert response.status_code == 302
        count = models.MapIdea.objects.all().count()
        assert count == 0

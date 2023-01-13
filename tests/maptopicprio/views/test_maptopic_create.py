import pytest
from django.urls import reverse

from adhocracy4.test.helpers import assert_template_response
from adhocracy4.test.helpers import freeze_phase
from adhocracy4.test.helpers import freeze_pre_phase
from adhocracy4.test.helpers import redirect_target
from meinberlin.apps.maptopicprio import models
from meinberlin.apps.maptopicprio import phases


@pytest.mark.django_db
def test_anonymous_cannot_create_maptopic(client, phase_factory):
    phase = phase_factory(phase_content=phases.PrioritizePhase())
    module = phase.module
    url = reverse("a4dashboard:maptopic-create", kwargs={"module_slug": module.slug})
    with freeze_phase(phase):
        count = models.MapTopic.objects.all().count()
        assert count == 0
        response = client.get(url)
        assert response.status_code == 302
        assert redirect_target(response) == "account_login"


@pytest.mark.django_db
def test_user_cannot_create_maptopic(client, phase_factory, user):
    phase = phase_factory(phase_content=phases.PrioritizePhase())
    module = phase.module
    url = reverse("a4dashboard:maptopic-create", kwargs={"module_slug": module.slug})
    with freeze_phase(phase):
        response = client.get(url)
        assert response.status_code == 302
        client.login(username=user.email, password="password")
        response = client.get(url)
        assert response.status_code == 403


@pytest.mark.django_db
def test_admin_can_create_maptopic(
    client, phase_factory, category_factory, admin, area_settings_factory
):
    phase = phase_factory(phase_content=phases.PrioritizePhase())
    module = phase.module
    area_settings_factory(module=module)
    category = category_factory(module=module)
    url = reverse("a4dashboard:maptopic-create", kwargs={"module_slug": module.slug})
    with freeze_phase(phase):
        client.login(username=admin.email, password="password")
        response = client.get(url)
        assert_template_response(
            response, "meinberlin_maptopicprio/maptopic_create_form.html"
        )
        maptopic = {
            "name": "MapTopic",
            "description": "description",
            "category": category.pk,
            "point": (0, 0),
            "point_label": "somewhere",
        }
        response = client.post(url, maptopic)
        assert response.status_code == 302
        assert redirect_target(response) == "maptopic-list"
        count = models.MapTopic.objects.all().count()
        assert count == 1


@pytest.mark.django_db
def test_moderator_cannot_create_maptopic_before_phase(
    client, phase_factory, category_factory, admin, area_settings_factory
):
    phase = phase_factory(phase_content=phases.PrioritizePhase())
    module = phase.module
    project = module.project
    moderator = project.moderators.first()
    url = reverse("a4dashboard:maptopic-create", kwargs={"module_slug": module.slug})
    with freeze_pre_phase(phase):
        client.login(username=moderator.email, password="password")
        response = client.get(url)
        assert response.status_code == 403


@pytest.mark.django_db
def test_initiator_can_always_create_maptopic(
    client, phase_factory, category_factory, area_settings_factory
):
    phase = phase_factory(phase_content=phases.PrioritizePhase())
    module = phase.module
    project = module.project
    area_settings_factory(module=module)
    category = category_factory(module=module)
    initiator = project.organisation.initiators.first()
    url = reverse("a4dashboard:maptopic-create", kwargs={"module_slug": module.slug})
    client.login(username=initiator.email, password="password")
    response = client.get(url)
    assert_template_response(
        response, "meinberlin_maptopicprio/maptopic_create_form.html"
    )
    maptopic = {
        "name": "MapTopic",
        "description": "description",
        "category": category.pk,
        "point": (0, 0),
        "point_label": "somewhere",
    }
    response = client.post(url, maptopic)
    assert response.status_code == 302
    assert redirect_target(response) == "maptopic-list"
    count = models.MapTopic.objects.all().count()
    assert count == 1

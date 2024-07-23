import pytest
from dateutil.parser import parse
from django.core.cache import cache
from django.urls import reverse
from django.utils import timezone
from freezegun import freeze_time

from adhocracy4.projects.enums import Access
from adhocracy4.projects.models import Project
from adhocracy4.test.helpers import assert_template_response
from meinberlin.apps.plans.models import Plan


@pytest.mark.django_db
def test_list_view(
    client,
    plan_factory,
    project_factory,
    external_project_factory,
    bplan_factory,
    phase_factory,
    user,
    apiclient,
):
    project_active = project_factory(name="active")
    project_private = project_factory(name="private", access=Access.PRIVATE)
    project_private.participants.add(user)
    project_private.save()
    project_semipublic = project_factory(name="semipublic", access=Access.SEMIPUBLIC)
    project_semipublic.participants.add(user)
    project_semipublic.save()
    project_future = project_factory(name="future")
    project_active_and_future = project_factory(name="active and future")
    project_past = project_factory(name="past")
    ep = external_project_factory(name="external project active", is_draft=False)
    external_project_factory(name="external project no phase", is_draft=False)
    bplan = bplan_factory(name="bplan", is_draft=False)
    plan_factory(title="plan")

    now = parse("2013-01-01 18:00:00 UTC")
    yesterday = now - timezone.timedelta(days=1)
    last_week = now - timezone.timedelta(days=7)
    tomorrow = now + timezone.timedelta(days=1)
    next_week = now + timezone.timedelta(days=7)

    # active phase
    phase_factory(
        start_date=last_week,
        end_date=next_week,
        module__project=project_active,
    )

    # active phase
    phase_factory(
        start_date=last_week,
        end_date=next_week,
        module__project=project_private,
    )

    # active phase
    phase_factory(
        start_date=last_week,
        end_date=next_week,
        module__project=project_semipublic,
    )

    # active phase
    phase_factory(start_date=last_week, end_date=next_week, module__project=bplan)

    # active phase
    phase_factory(start_date=last_week, end_date=next_week, module__project=ep)

    # future phase
    phase_factory(
        start_date=tomorrow,
        end_date=next_week,
        module__project=project_future,
    )

    # active phase
    phase_factory(
        start_date=yesterday,
        end_date=tomorrow,
        module__project=project_active_and_future,
    )

    # future_phase
    phase_factory(
        start_date=tomorrow,
        end_date=next_week,
        module__project=project_active_and_future,
    )

    # past phase
    phase_factory(
        start_date=last_week,
        end_date=yesterday,
        module__project=project_past,
    )
    # clear cache as it's populated on project creation
    cache.clear()

    with freeze_time(now):
        assert Project.objects.all().count() == 9
        apiclient.force_authenticate(user=user)

        # query api for active projects
        url = reverse("projects-list") + "?status=activeParticipation"
        response = apiclient.get(url)
        items = response.data
        assert len(items) == 4
        assert items[0]["title"] == "active"
        assert items[1]["title"] == "semipublic"
        assert items[2]["title"] == "active and future"
        assert items[3]["title"] == "bplan"
        assert items[0]["type"] == "project"
        assert items[1]["type"] == "project"
        assert items[2]["type"] == "project"
        assert items[3]["type"] == "project"
        assert items[0]["subtype"] == "default"
        assert items[1]["subtype"] == "default"
        assert items[2]["subtype"] == "default"
        assert items[3]["subtype"] == "external"

        # query api for future projects
        url = reverse("projects-list") + "?status=futureParticipation"
        response = apiclient.get(url)
        items = response.data
        assert len(items) == 1

        assert items[0]["title"] == "future"
        assert items[0]["type"] == "project"
        assert items[0]["subtype"] == "default"

        # query api for past projects
        url = reverse("projects-list") + "?status=pastParticipation"
        response = apiclient.get(url)
        items = response.data
        assert len(items) == 1

        assert items[0]["title"] == "past"
        assert items[0]["type"] == "project"
        assert items[0]["subtype"] == "default"

        # query api for past plans
        url = reverse("plans-list")
        response = apiclient.get(url)
        items = response.data
        assert len(items) == 1

        assert items[0]["title"] == "plan"
        assert items[0]["type"] == "plan"
        assert items[0]["subtype"] == "plan"

        # query api for external projects
        url = reverse("extprojects-list")
        response = apiclient.get(url)
        items = response.data
        assert len(items) == 2

        assert items[0]["title"] == "external project no phase"
        assert items[1]["title"] == "external project active"
        assert items[0]["type"] == "project"
        assert items[1]["type"] == "project"
        assert items[0]["subtype"] == "external"
        assert items[1]["subtype"] == "external"

        url = reverse("privateprojects-list")
        response = apiclient.get(url)
        items = response.data
        assert len(items) == 1


@pytest.mark.django_db
def test_list_view_no_district(client, plan_factory):
    plan_factory()
    plan_factory(district=None)
    url = reverse("meinberlin_plans:plan-list")
    response = client.get(url)
    assert_template_response(response, "meinberlin_plans/plan_list.html")


@pytest.mark.django_db
def test_detail_view(client, plan_factory):
    plan = plan_factory()
    url = plan.get_absolute_url()
    response = client.get(url)
    assert_template_response(response, "meinberlin_plans/plan_detail.html")


@pytest.mark.django_db
def test_export_view(client, plan_factory, project_factory):
    project1 = project_factory()
    project2 = project_factory()
    project3 = project_factory()
    plan = plan_factory.create(projects=[project1, project2, project3])
    assert plan.projects.all().count() == 3
    organisation = plan.organisation
    plan_factory(organisation=organisation)
    assert Plan.objects.all().count() == 2
    initiator = organisation.initiators.first()
    client.login(username=initiator.email, password="password")
    url = reverse(
        "a4dashboard:plan-export", kwargs={"organisation_slug": organisation.slug}
    )
    response = client.get(url)
    assert response.status_code == 200
    assert (
        response["Content-Type"] == "application/vnd.openxmlformats-officedocument."
        "spreadsheetml.sheet"
    )

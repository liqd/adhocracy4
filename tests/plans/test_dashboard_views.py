import pytest
from django.urls import reverse

from adhocracy4.projects.models import Topic
from adhocracy4.test.helpers import assert_template_response
from adhocracy4.test.helpers import redirect_target
from meinberlin.apps.plans.models import Plan


@pytest.mark.django_db
def test_initiator_can_edit(client, plan_factory):
    plan = plan_factory()
    initiator = plan.organisation.initiators.first()
    url = reverse(
        "a4dashboard:plan-update",
        kwargs={"organisation_slug": plan.organisation.slug, "pk": plan.pk},
    )
    client.login(username=initiator.email, password="password")
    response = client.get(url)
    assert_template_response(response, "meinberlin_plans/plan_update_form.html")

    data = {
        "title": "my plan title",
        "description_image": "",
        "description_image_copyright": "",
        "contact_address_text": "Some address",
        "contact_name": "Some name",
        "contact_phone": "",
        "contact_email": "me@example.com",
        "contact_url": "https://liqd.net/",
        "point": "",
        "point_label": "",
        "district": "",
        "cost": "1.000",
        "description": "this is a description",
        "topics": Topic.objects.first().pk,
        "status": plan.status,
        "participation": plan.participation,
        "participation_explanation": "Some explanation",
        "duration": "1 month",
    }
    response = client.post(url, data)
    assert redirect_target(response) == "plan-update"
    plan.refresh_from_db()
    assert plan.topics.all().count() == 1
    assert plan.topics.first().pk == data.get("topics")
    assert plan.title == data.get("title")
    assert plan.description == data.get("description")


@pytest.mark.django_db
def test_group_member_can_edit(
    client, plan_factory, user_factory, group_factory, organisation
):
    group1 = group_factory()
    group2 = group_factory()
    group_member = user_factory.create(groups=(group1, group2))
    organisation.groups.add(group2)
    plan = plan_factory(group=group2, organisation=organisation)

    url = reverse(
        "a4dashboard:plan-update",
        kwargs={"organisation_slug": organisation.slug, "pk": plan.pk},
    )
    client.login(username=group_member.email, password="password")
    response = client.get(url)
    assert_template_response(response, "meinberlin_plans/plan_update_form.html")

    data = {
        "title": "my plan title",
        "description_image": "",
        "description_image_copyright": "",
        "contact_address_text": "me@example.com",
        "point": "",
        "point_label": "",
        "district": "",
        "cost": "1.000",
        "description": "this is a description",
        "topics": Topic.objects.first().pk,
        "status": plan.status,
        "participation": plan.participation,
        "participation_explanation": "Some explanation",
        "duration": "1 month",
    }
    response = client.post(url, data)
    assert redirect_target(response) == "plan-update"
    plan.refresh_from_db()
    assert plan.topics.all().count() == 1
    assert plan.topics.first().pk == data.get("topics")
    assert plan.title == data.get("title")
    assert plan.description == data.get("description")
    assert plan.duration == data.get("duration")
    assert plan.group == group2


@pytest.mark.django_db
def test_initiator_can_create(client, organisation):
    initiator = organisation.initiators.first()
    url = reverse(
        "a4dashboard:plan-create", kwargs={"organisation_slug": organisation.slug}
    )
    client.login(username=initiator.email, password="password")
    response = client.get(url)
    assert_template_response(response, "meinberlin_plans/plan_create_dashboard.html")

    data = {
        "title": "my plan title",
        "description_image": "",
        "description_image_copyright": "",
        "contact_address_text": "me@example.com",
        "contact_name": "Some name",
        "contact_phone": "",
        "contact_email": "me@example.com",
        "contact_url": "https://liqd.net/",
        "point": "",
        "point_label": "",
        "district": "",
        "cost": "1.000",
        "description": "this is a description",
        "topics": Topic.objects.first().pk,
        "status": 0,
        "participation": 2,
        "participation_explanation": "Some explanation",
        "duration": "1 month",
    }
    response = client.post(url, data)
    assert redirect_target(response) == "plan-update"
    plan = Plan.objects.all().first()
    assert plan.topics.all().count() == 1
    assert plan.topics.first().pk == data.get("topics")
    assert plan.title == data.get("title")
    assert plan.description == data.get("description")
    assert plan.duration == data.get("duration")
    assert not plan.group


@pytest.mark.django_db
def test_group_member_can_create(client, organisation, user_factory, group_factory):
    group1 = group_factory()
    group2 = group_factory()
    group_member = user_factory.create(groups=(group1, group2))
    organisation.groups.add(group2)
    url = reverse(
        "a4dashboard:plan-create", kwargs={"organisation_slug": organisation.slug}
    )
    client.login(username=group_member.email, password="password")
    response = client.get(url)
    assert_template_response(response, "meinberlin_plans/plan_create_dashboard.html")

    data = {
        "title": "my plan title",
        "description_image": "",
        "description_image_copyright": "",
        "contact_address_text": "me@example.com",
        "contact_name": "Some name",
        "contact_phone": "",
        "contact_email": "me@example.com",
        "contact_url": "https://liqd.net/",
        "point": "",
        "point_label": "",
        "district": "",
        "cost": "1.000",
        "description": "this is a description",
        "topics": Topic.objects.first().pk,
        "status": 0,
        "participation": 2,
        "participation_explanation": "Some explanation",
        "duration": "1 month",
    }
    response = client.post(url, data)
    assert redirect_target(response) == "plan-update"
    plan = Plan.objects.all().first()
    assert plan.topics.all().count() == 1
    assert plan.topics.first().pk == data.get("topics")
    assert plan.title == data.get("title")
    assert plan.description == data.get("description")
    assert plan.duration == data.get("duration")
    assert plan.group == group2

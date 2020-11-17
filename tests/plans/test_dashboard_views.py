import pytest
from django.conf import settings
from django.urls import reverse

from adhocracy4.test.helpers import redirect_target
from meinberlin.apps.plans.models import Plan
from meinberlin.test.helpers import assert_template_response


@pytest.mark.django_db
def test_initiator_can_edit(client, plan_factory):
    plan = plan_factory()
    initiator = plan.organisation.initiators.first()
    url = reverse('a4dashboard:plan-update',
                  kwargs={'organisation_slug': plan.organisation.slug,
                          'pk': plan.pk})
    client.login(username=initiator.email, password='password')
    response = client.get(url)
    assert_template_response(
        response, 'meinberlin_plans/plan_update_form.html')

    choices = settings.A4_PROJECT_TOPICS
    data = {
        'title': 'my plan title',
        'description_image': '',
        'description_image_copyright': '',
        'contact': 'me@example.com',
        'point': '',
        'point_label': '',
        'district': '',
        'cost': '1.000',
        'description': 'this is a description',
        'topics': choices[0][0],
        'status': plan.status,
        'participation': plan.participation
    }
    response = client.post(url, data)
    assert redirect_target(response) == 'plan-list'
    plan.refresh_from_db()
    assert plan.topics == [data.get('topics')]
    assert plan.title == data.get('title')
    assert plan.description == data.get('description')


@pytest.mark.django_db
def test_group_member_can_edit(client, plan_factory, user_factory,
                               group_factory, organisation):
    group1 = group_factory()
    group2 = group_factory()
    group_member = user_factory.create(groups=(group1, group2))
    organisation.groups.add(group2)
    plan = plan_factory(group=group2, organisation=organisation)

    url = reverse('a4dashboard:plan-update',
                  kwargs={'organisation_slug': organisation.slug,
                          'pk': plan.pk})
    client.login(username=group_member.email, password='password')
    response = client.get(url)
    assert_template_response(
        response, 'meinberlin_plans/plan_update_form.html')

    choices = settings.A4_PROJECT_TOPICS
    data = {
        'title': 'my plan title',
        'description_image': '',
        'description_image_copyright': '',
        'contact': 'me@example.com',
        'point': '',
        'point_label': '',
        'district': '',
        'cost': '1.000',
        'description': 'this is a description',
        'topics': choices[0][0],
        'status': plan.status,
        'participation': plan.participation
    }
    response = client.post(url, data)
    assert redirect_target(response) == 'plan-list'
    plan.refresh_from_db()
    assert plan.topics == [data.get('topics')]
    assert plan.title == data.get('title')
    assert plan.description == data.get('description')
    assert plan.group == group2


@pytest.mark.django_db
def test_initiator_can_create(client, organisation):
    initiator = organisation.initiators.first()
    url = reverse('a4dashboard:plan-create',
                  kwargs={'organisation_slug': organisation.slug})
    client.login(username=initiator.email, password='password')
    response = client.get(url)
    assert_template_response(
        response, 'meinberlin_plans/plan_create_dashboard.html')

    choices = settings.A4_PROJECT_TOPICS
    data = {
        'title': 'my plan title',
        'description_image': '',
        'description_image_copyright': '',
        'contact': 'me@example.com',
        'point': '',
        'point_label': '',
        'district': '',
        'cost': '1.000',
        'description': 'this is a description',
        'topics': choices[0][0],
        'status': 0,
        'participation': 2
    }
    response = client.post(url, data)
    assert redirect_target(response) == 'plan-list'
    plan = Plan.objects.all().first()
    assert plan.topics == [data.get('topics')]
    assert plan.title == data.get('title')
    assert plan.description == data.get('description')
    assert not plan.group


@pytest.mark.django_db
def test_group_member_can_create(client, organisation, user_factory,
                                 group_factory):
    group1 = group_factory()
    group2 = group_factory()
    group_member = user_factory.create(groups=(group1, group2))
    organisation.groups.add(group2)
    url = reverse('a4dashboard:plan-create',
                  kwargs={'organisation_slug': organisation.slug})
    client.login(username=group_member.email, password='password')
    response = client.get(url)
    assert_template_response(
        response, 'meinberlin_plans/plan_create_dashboard.html')

    choices = settings.A4_PROJECT_TOPICS
    data = {
        'title': 'my plan title',
        'description_image': '',
        'description_image_copyright': '',
        'contact': 'me@example.com',
        'point': '',
        'point_label': '',
        'district': '',
        'cost': '1.000',
        'description': 'this is a description',
        'topics': choices[0][0],
        'status': 0,
        'participation': 2
    }
    response = client.post(url, data)
    assert redirect_target(response) == 'plan-list'
    plan = Plan.objects.all().first()
    assert plan.topics == [data.get('topics')]
    assert plan.title == data.get('title')
    assert plan.description == data.get('description')
    assert plan.group == group2

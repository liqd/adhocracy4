import pytest
from django.core.urlresolvers import reverse

from meinberlin.apps.plans.models import Plan
from meinberlin.test.helpers import assert_template_response


@pytest.mark.django_db
def test_list_view(client, plan_factory):
    plan_factory()
    url = reverse('meinberlin_plans:plan-list')
    response = client.get(url)
    assert_template_response(
        response, 'meinberlin_plans/plan_list.html')


@pytest.mark.django_db
def test_list_view_no_district(client, plan_factory):
    plan_factory()
    plan_factory(district=None)
    url = reverse('meinberlin_plans:plan-list')
    response = client.get(url)
    assert_template_response(
        response, 'meinberlin_plans/plan_list.html')


@pytest.mark.django_db
def test_export_view(client, plan_factory, project_factory):
    project1 = project_factory()
    project2 = project_factory()
    project3 = project_factory()
    plan = plan_factory.create(projects=[project1, project2, project3])
    assert plan.projects.all().count() == 3
    plan_factory()
    assert Plan.objects.all().count() == 2
    url = reverse('meinberlin_plans:plan-export')
    response = client.get(url)
    assert response['content-type'] == \
        'application/vnd.openxmlformats-' \
        'officedocument.spreadsheetml.sheet'


@pytest.mark.django_db
def test_detail_view(client, plan_factory):
    plan = plan_factory()
    url = plan.get_absolute_url()
    response = client.get(url)
    assert_template_response(
        response, 'meinberlin_plans/plan_detail.html')

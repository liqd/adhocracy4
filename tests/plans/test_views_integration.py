import pytest
from django.core.urlresolvers import reverse

from meinberlin.test.helpers import assert_template_response


@pytest.mark.django_db
def test_list_view(client, plan_factory):
    plan_factory()
    url = reverse('meinberlin_plans:plan-list')
    response = client.get(url)
    assert_template_response(
        response, 'meinberlin_plans/plan_list.html')


@pytest.mark.django_db
def test_detail_view(client, plan_factory):
    plan = plan_factory()
    url = plan.get_absolute_url()
    response = client.get(url)
    assert_template_response(
        response, 'meinberlin_plans/plan_detail.html')

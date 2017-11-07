import pytest
from django.core.urlresolvers import reverse


@pytest.mark.django_db
def test_list_view(client, plan_factory):
    plan_factory()
    url = reverse('meinberlin_plans:plan-list')
    response = client.get(url)
    assert response.status_code == 200
    assert response.template_name[0] == 'meinberlin_plans/plan_list.html'


@pytest.mark.django_db
def test_detail_view(client, plan):
    url = reverse('meinberlin_plans:plan-detail', kwargs={
        'slug': plan.slug
    })
    response = client.get(url)
    assert response.status_code == 200
    assert response.template_name[0] == 'meinberlin_plans/plan_detail.html'

import pytest
from django.urls import reverse

from adhocracy4.test.helpers import redirect_target


@pytest.mark.django_db
def test_plan_publish_perms(client, plan, user, user2):
    publish_url = reverse('a4dashboard:plan-publish', kwargs={
        'pk': plan.pk})

    data = {'action': 'publish'}

    response = client.post(publish_url, data)
    assert redirect_target(response) == 'account_login'

    client.login(username=user, password='password')
    response = client.post(publish_url, data)
    assert response.status_code == 403

    organisation = plan.organisation
    organisation.initiators.add(user2)
    client.login(username=user2, password='password')
    response = client.post(publish_url, data)
    assert redirect_target(response) == 'plan-update'


@pytest.mark.django_db
def test_plan_publish(client, plan_factory, user2):
    plan = plan_factory(is_draft=True)
    organisation = plan.organisation
    organisation.initiators.add(user2)

    publish_url = reverse('a4dashboard:plan-publish', kwargs={
        'pk': plan.pk})

    data = {'action': 'publish'}

    client.login(username=user2, password='password')
    response = client.post(publish_url, data)
    assert redirect_target(response) == 'plan-update'

    plan.refresh_from_db()
    assert plan.is_draft is False


@pytest.mark.django_db
def test_plan_unpublish(client, plan_factory, user2):
    plan = plan_factory(is_draft=False)
    organisation = plan.organisation
    organisation.initiators.add(user2)

    publish_url = reverse('a4dashboard:plan-publish', kwargs={
        'pk': plan.pk})

    data = {'action': 'unpublish'}

    client.login(username=user2, password='password')
    response = client.post(publish_url, data)
    assert redirect_target(response) == 'plan-update'

    plan.refresh_from_db()
    assert plan.is_draft is True

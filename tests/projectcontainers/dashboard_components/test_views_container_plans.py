import pytest

from adhocracy4.dashboard import components
from adhocracy4.test.helpers import redirect_target
from meinberlin.test.helpers import assert_dashboard_form_component_response
from meinberlin.test.helpers import setup_group_members

component = components.projects.get('plans')


@pytest.mark.django_db
def test_edit_view(client, plan_factory, project_container):
    initiator = project_container.organisation.initiators.first()
    organisation = project_container.organisation
    plan = plan_factory(organisation=organisation)
    url = component.get_base_url(project_container)
    client.login(username=initiator.email, password='password')
    response = client.get(url)
    assert_dashboard_form_component_response(response, component)

    data = {
        'plans': plan.pk
    }
    response = client.post(url, data)
    assert redirect_target(response) == 'dashboard-plans-edit'
    project_container.refresh_from_db()
    assert list(project_container.plans.all()) == [plan]
    assert project_container.project_type == \
        'meinberlin_projectcontainers.ProjectContainer'


@pytest.mark.django_db
def test_edit_view_group_member(client, plan_factory, project_container,
                                group_factory, user_factory):
    project_container, _, group_member_in_pro, _ = \
        setup_group_members(project_container, group_factory, user_factory)
    organisation = project_container.organisation
    plan = plan_factory(organisation=organisation)
    url = component.get_base_url(project_container)
    client.login(username=group_member_in_pro.email, password='password')
    response = client.get(url)
    assert_dashboard_form_component_response(response, component)

    data = {
        'plans': plan.pk
    }
    response = client.post(url, data)
    assert redirect_target(response) == 'dashboard-plans-edit'
    project_container.refresh_from_db()
    assert list(project_container.plans.all()) == [plan]
    assert project_container.project_type == \
        'meinberlin_projectcontainers.ProjectContainer'

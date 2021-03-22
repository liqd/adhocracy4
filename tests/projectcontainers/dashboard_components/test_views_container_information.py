import pytest

from adhocracy4.dashboard import components
from meinberlin.test.helpers import assert_dashboard_form_component_edited
from meinberlin.test.helpers import assert_dashboard_form_component_response
from meinberlin.test.helpers import setup_group_member

component = components.projects.get('container-information')


@pytest.mark.django_db
def test_edit_view(client, project, project_container_factory):
    project_container = project_container_factory(projects=[project])
    initiator = project_container.organisation.initiators.first()
    url = component.get_base_url(project_container)
    client.login(username=initiator.email, password='password')
    response = client.get(url)
    assert_dashboard_form_component_response(response, component)

    data = {
        'information': 'test',
    }
    response = client.post(url, data)
    assert_dashboard_form_component_edited(
        response, component, project_container, data)
    assert project_container.project_type == \
        'meinberlin_projectcontainers.ProjectContainer'


@pytest.mark.django_db
def test_edit_view_group_member(client, project, project_container_factory,
                                group_factory, user_factory):
    project_container = project_container_factory(projects=[project])
    group_member, _, project_container = setup_group_member(
        None, project_container, group_factory, user_factory)
    url = component.get_base_url(project_container)
    client.login(username=group_member.email, password='password')
    response = client.get(url)
    assert_dashboard_form_component_response(response, component)

    data = {
        'information': 'test',
    }
    response = client.post(url, data)
    assert_dashboard_form_component_edited(
        response, component, project_container, data)
    assert project_container.project_type == \
        'meinberlin_projectcontainers.ProjectContainer'

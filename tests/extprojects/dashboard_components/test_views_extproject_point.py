import json

import pytest

from adhocracy4.dashboard import components
from adhocracy4.test.helpers import redirect_target
from meinberlin.test.helpers import assert_dashboard_form_component_response
from meinberlin.test.helpers import setup_group_members

component = components.projects.get('point')


@pytest.mark.django_db
def test_edit_view(client, external_project, administrative_district):
    initiator = external_project.organisation.initiators.first()
    url = component.get_base_url(external_project)
    client.login(username=initiator.email, password='password')
    response = client.get(url)
    assert_dashboard_form_component_response(response, component)

    data = {
        'administrative_district': administrative_district.pk,
        'point': '{"type":"Feature","properties":{},'
                 '"geometry":{"type":"Point",'
                 '"coordinates":[13.382721,52.512121]}}'
    }
    response = client.post(url, data)
    assert redirect_target(response) == 'dashboard-point-edit'
    external_project.refresh_from_db()
    assert external_project.administrative_district == \
        administrative_district
    point = external_project.point
    data = json.loads(data.get('point'))

    for key in point.keys():
        assert point[key] == data[key]

    assert external_project.project_type == \
        'meinberlin_extprojects.ExternalProject'


@pytest.mark.django_db
def test_edit_view_group_member(
        client, external_project, administrative_district,
        group_factory, user_factory):
    external_project, _, group_member_in_pro, _ = \
        setup_group_members(external_project, group_factory, user_factory)
    url = component.get_base_url(external_project)
    client.login(username=group_member_in_pro.email, password='password')
    response = client.get(url)
    assert_dashboard_form_component_response(response, component)

    data = {
        'administrative_district': administrative_district.pk,
        'point': '{"type":"Feature","properties":{},'
                 '"geometry":{"type":"Point",'
                 '"coordinates":[13.382721,52.512121]}}'
    }
    response = client.post(url, data)
    assert redirect_target(response) == 'dashboard-point-edit'
    external_project.refresh_from_db()
    assert external_project.administrative_district == \
        administrative_district
    point = external_project.point
    data = json.loads(data.get('point'))

    for key in point.keys():
        assert point[key] == data[key]

    assert external_project.project_type == \
        'meinberlin_extprojects.ExternalProject'

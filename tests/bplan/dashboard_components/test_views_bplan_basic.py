import pytest
from dateutil.parser import parse
from django.core import mail

from adhocracy4.dashboard import components
from adhocracy4.test.helpers import redirect_target
from meinberlin.apps.bplan.phases import StatementPhase
from meinberlin.test.helpers import assert_dashboard_form_component_response
from meinberlin.test.helpers import setup_group_members

component = components.projects.get("bplan")


@pytest.mark.django_db
def test_edit_view(client, phase_factory, bplan, module_factory):
    module = module_factory(project=bplan)
    phase = phase_factory(phase_content=StatementPhase(), module=module)
    initiator = bplan.organisation.initiators.first()
    url = component.get_base_url(bplan)
    client.login(username=initiator.email, password="password")
    response = client.get(url)
    assert_dashboard_form_component_response(response, component)
    assert len(mail.outbox) == 1

    data = {
        "name": "name",
        "description": "desc",
        "identifier": "VE69 5a BPLAN",
        "image_copyright": "copyright",
        "tile_image_copyright": "tile_copyright",
        "is_archived": False,
        "is_public": True,
        "url": "https://foo.bar",
        "office_worker_email": "test@foo.bar",
        "start_date_0": "2013-01-01",
        "start_date_1": "18:00",
        "end_date_0": "2013-01-10",
        "end_date_1": "18:00",
    }
    response = client.post(url, data)
    assert redirect_target(response) == "dashboard-bplan-project-edit"
    bplan.refresh_from_db()
    assert bplan.name == data.get("name")
    assert bplan.description == data.get("description")
    assert bplan.identifier == data.get("identifier")
    assert bplan.tile_image_copyright == data.get("tile_image_copyright")
    assert bplan.is_archived == data.get("is_archived")
    assert bplan.is_public == data.get("is_public")
    assert bplan.url == data.get("url")
    assert bplan.office_worker_email == data.get("office_worker_email")
    phase.refresh_from_db()
    assert phase.start_date == parse("2013-01-01 17:00:00 UTC")
    assert phase.end_date == parse("2013-01-10 17:00:00 UTC")
    assert bplan.project_type == "meinberlin_bplan.Bplan"
    assert len(mail.outbox) == 2
    assert mail.outbox[1].to == ["test@foo.bar"]


@pytest.mark.django_db
def test_edit_view_group_member(
    client, phase_factory, bplan, module_factory, group_factory, user_factory
):
    module = module_factory(project=bplan)
    phase = phase_factory(phase_content=StatementPhase(), module=module)
    bplan, _, group_member_in_pro, _ = setup_group_members(
        bplan, group_factory, user_factory
    )
    url = component.get_base_url(bplan)
    client.login(username=group_member_in_pro.email, password="password")
    response = client.get(url)
    assert_dashboard_form_component_response(response, component)
    assert len(mail.outbox) == 1

    data = {
        "name": "name",
        "description": "desc",
        "identifier": "VE69 5a BPLAN",
        "image_copyright": "copyright",
        "tile_image_copyright": "tile_copyright",
        "is_archived": False,
        "is_public": True,
        "url": "https://foo.bar",
        "office_worker_email": "test@foo.bar",
        "start_date_0": "2013-01-01",
        "start_date_1": "18:00",
        "end_date_0": "2013-01-10",
        "end_date_1": "18:00",
    }
    response = client.post(url, data)
    assert redirect_target(response) == "dashboard-bplan-project-edit"
    bplan.refresh_from_db()
    assert bplan.name == data.get("name")
    assert bplan.description == data.get("description")
    assert bplan.identifier == data.get("identifier")
    assert bplan.tile_image_copyright == data.get("tile_image_copyright")
    assert bplan.is_archived == data.get("is_archived")
    assert bplan.is_public == data.get("is_public")
    assert bplan.url == data.get("url")
    assert bplan.office_worker_email == data.get("office_worker_email")
    phase.refresh_from_db()
    assert phase.start_date == parse("2013-01-01 17:00:00 UTC")
    assert phase.end_date == parse("2013-01-10 17:00:00 UTC")
    assert bplan.project_type == "meinberlin_bplan.Bplan"
    assert len(mail.outbox) == 2
    assert mail.outbox[1].to == ["test@foo.bar"]

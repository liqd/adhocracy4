import json

import pytest
from django.utils.translation import gettext as _

from adhocracy4.exports import unescape_and_strip_html
from adhocracy4.projects.models import Topic
from meinberlin.apps.plans.exports import DashboardPlanExportView


@pytest.mark.django_db
def test_reply_to_mixin(plan_factory, project_factory, administrative_district):
    export = DashboardPlanExportView()
    virtual = export.get_virtual_fields({})
    # ItemExportWithReferenceNumberMixin and ItemExportWithLinkMixin
    assert "reference_number" in virtual
    assert "link" in virtual
    # ExportModelFieldsMixin, set in fields
    assert "title" in virtual
    assert "description" in virtual
    assert "contact_name" in virtual
    assert "contact_address_text" in virtual
    assert "contact_phone" in virtual
    assert "contact_email" in virtual
    assert "contact_url" in virtual
    assert "district" in virtual
    assert "topics" in virtual
    assert "cost" in virtual
    assert "duration" in virtual
    assert "status" in virtual
    assert "participation" in virtual
    assert "participation_explanation" in virtual
    assert "organisation_name" in virtual
    assert "created" in virtual
    assert "modified" in virtual
    assert "is_draft" in virtual
    # ItemExportWithLocationMixin
    assert "location_lon" in virtual
    assert "location_lat" in virtual
    assert "location_label" in virtual
    # defined directly in DashboardPlanExportView
    assert "projects" in virtual
    assert "projects_links" in virtual

    plan = plan_factory(point="")

    # ItemExportWithReferenceNumberMixin and ItemExportWithLinkMixin
    assert plan.reference_number == export.get_reference_number_data(plan)
    # ItemExportWithLinkMixin cannot be tested easily (needs a request)
    # and should be tested in a4 anyway

    # ExportModelFieldsMixin, set in fields
    assert str(plan.title) == export.get_field_data(plan, "title")
    assert plan.topics.all().count() == 0
    assert export.get_field_data(plan, "topics") == ""
    assert plan.cost == export.get_field_data(plan, "cost")
    duration = plan.duration
    if duration is None:
        duration = ""
    assert str(duration) == export.get_field_data(plan, "duration")
    # get_..._data methods overwritten in DashboardPlanExportView
    assert unescape_and_strip_html(plan.description) == export.get_description_data(
        plan
    )
    assert plan.contact_name == export.get_field_data(plan, "contact_name")
    assert unescape_and_strip_html(
        plan.contact_address_text
    ) == export.get_contact_address_text_data(plan)
    assert plan.contact_phone == export.get_field_data(plan, "contact_phone")
    assert plan.contact_email == export.get_field_data(plan, "contact_email")
    assert plan.contact_url == export.get_field_data(plan, "contact_url")
    district = plan.district.name if plan.district else str("City wide")
    assert district == export.get_district_data(plan)
    assert plan.get_status_display() == export.get_status_data(plan)
    assert plan.get_participation_display() == export.get_participation_data(plan)
    assert plan.participation_explanation == export.get_field_data(
        plan, "participation_explanation"
    )
    assert plan.organisation.name == export.get_organisation_name_data(plan)
    assert plan.created.astimezone().isoformat() == export.get_field_data(
        plan, "created"
    )
    assert plan.modified.astimezone().isoformat() == export.get_field_data(
        plan, "modified"
    )
    assert _("no") == export.get_field_data(plan, "is_draft")
    # ItemExportWithLocationMixin
    assert "" == export.get_location_lon_data(plan)
    assert "" == export.get_location_lat_data(plan)
    assert plan.point_label == export.get_location_label_data(plan)
    # defined directly in DashboardPlanExportView
    assert "" == export.get_projects_data(plan)
    assert "" == export.get_projects_links_data(plan)

    project_1 = project_factory()
    project_2 = project_factory()
    plan = plan_factory(
        contact_name="Joe",
        contact_address_text="<i>me@example.com</i>",
        contact_phone="12345678",
        contact_email="<i>me@example.com</i>",
        contact_url="https://liqd.net",
        description="this is a description<br>with a newline",
        topics=[Topic.objects.first()],
        status=0,
        participation=2,
        participation_explanation="this is some explanation",
        duration="1 month",
        projects=[project_1, project_2],
        district=administrative_district,
        point=json.loads(
            '{"type":"Feature","properties":{},'
            '"geometry":{"type":"Point",'
            '"coordinates":[13.382721,52.512121]}}'
        ),
        is_draft=True,
    )

    # ItemExportWithReferenceNumberMixin and ItemExportWithLinkMixin
    assert plan.reference_number == export.get_reference_number_data(plan)
    # ItemExportWithLinkMixin cannot be tested easily (needs a request)
    # and should be tested in a4 anyway

    # ExportModelFieldsMixin, set in fields
    assert str(plan.title) == export.get_field_data(plan, "title")
    assert plan.topics.all().count() == 1
    assert str(plan.topics.first()) == export.get_field_data(plan, "topics")
    assert plan.cost == export.get_field_data(plan, "cost")
    duration = plan.duration
    if duration is None:
        duration = ""
    assert str(duration) == export.get_field_data(plan, "duration")
    # get_..._data methods overwritten in DashboardPlanExportView
    assert unescape_and_strip_html(plan.description) == export.get_description_data(
        plan
    )
    assert plan.contact_name == export.get_field_data(plan, "contact_name")
    assert unescape_and_strip_html(
        plan.contact_address_text
    ) == export.get_contact_address_text_data(plan)
    assert plan.contact_phone == export.get_field_data(plan, "contact_phone")
    assert plan.contact_email == export.get_field_data(plan, "contact_email")
    assert plan.contact_url == export.get_field_data(plan, "contact_url")
    district = plan.district.name if plan.district else str("City wide")
    assert district == export.get_district_data(plan)
    assert plan.get_status_display() == export.get_status_data(plan)
    assert plan.get_participation_display() == export.get_participation_data(plan)
    assert plan.participation_explanation == export.get_field_data(
        plan, "participation_explanation"
    )
    assert plan.organisation.name == export.get_organisation_name_data(plan)
    assert plan.created.astimezone().isoformat() == export.get_field_data(
        plan, "created"
    )
    assert plan.modified.astimezone().isoformat() == export.get_field_data(
        plan, "modified"
    )
    assert _("yes") == export.get_field_data(plan, "is_draft")
    # ItemExportWithLocationMixin
    assert 13.382721 == export.get_location_lon_data(plan)
    assert 52.512121 == export.get_location_lat_data(plan)
    assert plan.point_label == export.get_location_label_data(plan)

    # defined directly in DashboardPlanExportView
    projects = ""
    if plan.projects.all():
        projects = ", \n".join([project.name for project in plan.projects.all()])
    assert projects == export.get_projects_data(plan)

from django.utils import timezone
from django.utils.translation import gettext as _

from adhocracy4.dashboard import mixins as a4dashboard_mixins
from adhocracy4.exports import mixins
from adhocracy4.exports import views as export_views

from . import models


class DashboardPlanExportView(
    a4dashboard_mixins.DashboardBaseMixin,
    mixins.ItemExportWithReferenceNumberMixin,
    mixins.ItemExportWithLinkMixin,
    mixins.ExportModelFieldsMixin,
    mixins.ItemExportWithLocationMixin,
    export_views.BaseExport,
    export_views.AbstractXlsxExportView,
):
    permission_required = "meinberlin_plans.export_plan"
    model = models.Plan
    fields = [
        "title",
        "description",
        "contact_name",
        "contact_address_text",
        "contact_phone",
        "contact_email",
        "contact_url",
        "district",
        "cost",
        "duration",
        "status",
        "participation",
        "participation_explanation",
        "organisation",
        "created",
        "modified",
        "is_draft",
    ]
    html_fields = ["description", "contact_address_text"]
    related_fields = {"organisation": ["name"]}
    choice_fields = ["status", "participation"]

    def get_object_list(self):
        if self.organisation.has_initiator(self.request.user):
            return models.Plan.objects.filter(organisation=self.organisation)
        else:
            if self.organisation.groups.all() and self.request.user.groups.all():
                org_groups = self.organisation.groups.all()
                user_groups = self.request.user.groups.all()
                shared_groups = org_groups & user_groups
                group = shared_groups.distinct().first()
                return models.Plan.objects.filter(
                    organisation=self.organisation, group=group
                )

    def get_permission_object(self):
        return self.organisation

    def get_base_filename(self):
        return "plans_%s" % timezone.now().strftime("%Y%m%dT%H%M%S")

    def get_virtual_fields(self, virtual):
        virtual = super().get_virtual_fields(virtual)
        virtual["projects"] = _("Projects")
        virtual["projects_links"] = _("Project Links")
        virtual["is_draft"] = _("Draft")
        virtual["organisation_name"] = _("Organisation")
        virtual["topics"] = _("Topics")
        return virtual

    def get_district_data(self, item):
        return item.district.name if item.district else str(_("City wide"))

    def get_projects_data(self, item):
        if item.projects.all():
            return ", \n".join([project.name for project in item.projects.all()])
        return ""

    def get_topics_data(self, item):
        if item.topics.all():
            return ", \n".join([topic.name for topic in item.topics.all()])
        return ""

    def get_projects_links_data(self, item):
        if item.projects.all():
            return str(
                [
                    self.request.build_absolute_uri(project.get_absolute_url())
                    for project in item.projects.all()
                ]
            )
        return ""

from django.utils import timezone
from django.utils.translation import ugettext
from django.utils.translation import ugettext_lazy as _

from adhocracy4.dashboard import mixins as a4dashboard_mixins
from adhocracy4.exports import mixins as export_mixins
from adhocracy4.exports import unescape_and_strip_html
from adhocracy4.exports import views as export_views
from meinberlin.apps.exports import mixins as mb_export_mixins

from . import models


class DashboardPlanExportView(a4dashboard_mixins.DashboardBaseMixin,
                              mb_export_mixins.
                              ItemExportWithReferenceNumberMixin,
                              export_mixins.ItemExportWithLinkMixin,
                              export_mixins.ExportModelFieldsMixin,
                              export_mixins.ItemExportWithLocationMixin,
                              export_views.BaseExport,
                              export_views.AbstractXlsxExportView):

    permission_required = 'meinberlin_plans.export_plan'
    model = models.Plan
    fields = ['title', 'description', 'contact', 'district', 'topics',
              'cost', 'duration', 'status', 'participation', 'organisation']
    html_fields = ['description']

    def get_object_list(self):
        if self.organisation.has_initiator(self.request.user):
            return models.Plan.objects.filter(organisation=self.organisation)
        else:
            if self.organisation.groups.all() and \
               self.request.user.groups.all():
                org_groups = self.organisation.groups.all()
                user_groups = self.request.user.groups.all()
                shared_groups = org_groups & user_groups
                group = shared_groups.distinct().first()
                return models.Plan.objects\
                    .filter(organisation=self.organisation, group=group)

    def get_permission_object(self):
        return self.organisation

    def get_base_filename(self):
        return 'plans_%s' % timezone.now().strftime('%Y%m%dT%H%M%S')

    def get_virtual_fields(self, virtual):
        virtual = super().get_virtual_fields(virtual)
        virtual['projects'] = ugettext('Projects')
        virtual['projects_links'] = ugettext('Project Links')
        return virtual

    def get_organisation_data(self, item):
        return item.organisation.name

    def get_district_data(self, item):
        return item.district.name if item.district else str(_('City wide'))

    def get_contact_data(self, item):
        return unescape_and_strip_html(item.contact)

    def get_status_data(self, item):
        return item.get_status_display()

    def get_participation_data(self, item):
        return item.get_participation_display()

    def get_description_data(self, item):
        return unescape_and_strip_html(item.description)

    def get_projects_data(self, item):
        if item.projects.all():
            return ', \n'.join(
                [project.name
                 for project in item.projects.all()]
            )
        return ''

    def get_projects_links_data(self, item):
        if item.projects.all():
            return str([self.request.build_absolute_uri(
                        project.get_absolute_url())
                        for project in item.projects.all()
                        ])
        return ''

import csv

from django.http import HttpResponse
from django.utils.translation import ugettext as _
from django.views import generic

from adhocracy4.exports.views import VirtualFieldMixin
from adhocracy4.modules import models as module_models
from adhocracy4.rules import mixins as rules_mixins

from . import exports


class ExportModuleDispatcher(rules_mixins.PermissionRequiredMixin,
                             generic.View):
    permission_required = 'a4projects.change_project'

    def dispatch(self, request, *args, **kwargs):
        export_id = int(kwargs.pop('export_id'))
        module = module_models.Module.objects.get(slug=kwargs['module_slug'])
        project = module.project

        self.project = project

        # Since the PermissionRequiredMixin.dispatch method is never called
        # we have to check permissions manually
        if not self.has_permission():
            return self.handle_no_permission()

        module_exports = exports[module]
        assert len(module_exports) > export_id

        # Dispatch the request to the export view
        view = module_exports[export_id][1].as_view()
        return view(request, module=module, *args, **kwargs)

    def get_permission_object(self):
        return self.project


class AbstractCSVExportView(generic.View):
    def get_filename(self):
        return '%s.csv' % (self.get_base_filename())

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = \
            'attachment; filename="%s"' % self.get_filename()

        writer = csv.writer(response, lineterminator='\n',
                            quotechar='"', quoting=csv.QUOTE_ALL)
        writer.writerow(self.get_header())
        writer.writerows(self.export_rows())

        return response


class ItemExportWithModeratorFeedback(VirtualFieldMixin):
    def get_virtual_fields(self, virtual):
        if 'moderator_feedback' not in virtual:
            virtual['moderator_feedback'] = _('Moderator feedback')
        if 'moderator_statement' not in virtual:
            virtual['moderator_statement'] = _('Official Statement')
        return super().get_virtual_fields(virtual)

    def get_moderator_feedback_data(self, item):
        return item.get_moderator_feedback_display()

    def get_moderator_statement_data(self, item):
        if item.moderator_statement:
            # FIXME: would prefer to have a helper function instead of a class
            # method for unescape_and_strip
            return self.unescape_and_strip_html(
                item.moderator_statement.statement)
        return ''

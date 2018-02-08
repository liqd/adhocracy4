from django.views import generic

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

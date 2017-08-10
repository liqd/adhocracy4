from adhocracy4.projects import mixins as project_mixins
from adhocracy4.rules import mixins as rules_mixins

from . import models


class ModuleDetailView(rules_mixins.PermissionRequiredMixin,
                       project_mixins.ModuleDispatchMixin):
    model = models.Module
    permission_required = 'a4projects.view_project'
    slug_url_kwarg = 'module_slug'

    def get_permission_object(self):
        return self.project

    def get_context_data(self, **kwargs):
        """Append project and module to the template context."""
        if 'project' not in kwargs:
            kwargs['project'] = self.project
        if 'module' not in kwargs:
            kwargs['module'] = self.module
        return super().get_context_data(**kwargs)

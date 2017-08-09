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

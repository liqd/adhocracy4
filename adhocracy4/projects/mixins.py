from django.utils.functional import cached_property
from django.views import generic


class PhaseDispatchMixin(generic.DetailView):

    @cached_property
    def project(self):
        return self.get_object()

    @cached_property
    def module(self):
        return self.project.last_active_module

    def dispatch(self, request, *args, **kwargs):
        # Choose the appropriate view for the current active phase.
        kwargs['project'] = self.project
        kwargs['module'] = self.module

        return self._view_by_phase()(request, *args, **kwargs)

    def _view_by_phase(self):
        """
        Choose the appropriate view for the current active phase.
        """
        if self.module and self.module.last_active_phase:
            return self.module.last_active_phase.view.as_view()
        else:
            return super().dispatch


class ProjectMixin(generic.base.ContextMixin):
    def dispatch(self, *args, **kwargs):
        self.project = kwargs['project']
        self.module = kwargs['module']
        self.phase = self.module.last_active_phase if self.module else None
        # Workaround for filters
        self.request.module = self.module

        return super(ProjectMixin, self).dispatch(*args, **kwargs)

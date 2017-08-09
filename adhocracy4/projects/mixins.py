from django.views import generic


class PhaseDispatchMixin(generic.DetailView):
    def dispatch(self, request, *args, **kwargs):
        # Choose the appropriate view for the current active phase.
        project = self.get_object()
        kwargs['project'] = project
        module = project.last_active_module
        kwargs['module'] = module

        return self._view_by_phase(module)(request, *args, **kwargs)

    def _view_by_phase(self, module):
        """
        Choose the appropriate view for the current active phase.
        """
        if module:
            return module.last_active_phase.view.as_view()
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

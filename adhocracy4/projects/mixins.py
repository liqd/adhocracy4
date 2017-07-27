from django.views import generic


class PhaseDispatchMixin(generic.DetailView):
    def dispatch(self, request, *args, **kwargs):
        kwargs['project'] = self.get_object()
        return self._view_by_phase()(request, *args, **kwargs)

    def _view_by_phase(self):
        """
        Choose the appropriate view for the current active phase.
        """
        project = self.get_object()

        if project.last_active_module:
            return project.last_active_module.last_active_phase.view.as_view()
        else:
            return super().dispatch


class ProjectMixin(generic.base.ContextMixin):
    def dispatch(self, *args, **kwargs):
        self.project = kwargs['project']
        self.phase = self.project.active_phase or self.project.past_phases[0]
        self.module = self.phase.module if self.phase else None
        self.request.module = self.module
        return super(ProjectMixin, self).dispatch(*args, **kwargs)

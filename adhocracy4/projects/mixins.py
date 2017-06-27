from django.views import generic


class PhaseDispatcher(generic.DetailView):
    def dispatch(self, request, *args, **kwargs):
        kwargs['project'] = self.project
        return self._view_by_phase()(request, *args, **kwargs)

    def _view_by_phase(self):
        """Choose the appropriate view for the current active phase."""
        project = self.get_object()

        if project.active_phase:
            return project.active_phase.view.as_view()
        elif project.past_phases:
            return project.past_phases[0].view.as_view()
        else:
            return super(PhaseDispatcher, self).dispatch


class ProjectMixin(generic.base.ContextMixin):
    def dispatch(self, *args, **kwargs):
        self.project = kwargs['project']
        self.phase = self.project.active_phase or self.project.past_phases[0]
        self.module = self.phase.module if self.phase else None
        self.request.module = self.module
        return super(ProjectMixin, self).dispatch(*args, **kwargs)

from django.views import generic

from adhocracy4.modules.views import ModuleRedirectView


class ModuleDispatchMixin(generic.DetailView):
    def dispatch(self, request, *args, **kwargs):
        kwargs['project'] = self.get_object()
        project = self.get_object()
        if project.last_active_module:
            view = ModuleRedirectView.as_view()
        else:
            view = super().dispatch
        return view(request, *args, **kwargs)


class ProjectMixin(generic.base.ContextMixin):
    def dispatch(self, *args, **kwargs):
        self.project = kwargs['project']
        self.phase = self.project.active_phase or self.project.past_phases[0]
        self.module = self.phase.module if self.phase else None
        self.request.module = self.module
        return super(ProjectMixin, self).dispatch(*args, **kwargs)

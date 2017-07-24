from django.views import generic


class PhaseDispatchMixin(generic.DetailView):
    def dispatch(self, request, *args, **kwargs):
        kwargs['module'] = self.get_object()
        return self._view_by_phase()(request, *args, **kwargs)

    def _view_by_phase(self):
        """
        Choose the appropriate view for the current active phase.
        """
        mod = self.get_object()

        if mod.last_active_phase:
            return mod.last_active_phase.view.as_view()
        else:
            return super().dispatch

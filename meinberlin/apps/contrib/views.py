from django.shortcuts import redirect
from django.views import generic


class ComponentLibraryView(generic.base.TemplateView):
    template_name = 'meinberlin_contrib/component_library.html'


class CanonicalURLDetailView(generic.DetailView):
    """DetailView redirecting to the canonical absolute url of an object."""

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        # Redirect to the absolute url if it differs from the current path
        if hasattr(self.object, 'get_absolute_url'):
            absolute_url = self.object.get_absolute_url()
            if absolute_url != request.path:
                return redirect(absolute_url)

        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

from django.http import Http404
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.views import generic

from adhocracy4.modules.models import Module
from adhocracy4.projects.models import Project


class ProjectContextMixin(generic.base.ContextMixin):
    """Add project and module attributes to the view and the template context.

    This acts as a replacement of ProjectMixin and
    is a counterpart to the PhaseDispatcher logic.

    To consider the object context from get_object() set the
    get_context_from_object attribute. Enable this only if get_object() does
    not access the project and module properties.
    """

    project_lookup_field = 'slug'
    project_url_kwarg = 'project_slug'
    module_lookup_field = 'slug'
    module_url_kwarg = 'module_slug'
    get_context_from_object = False

    @property
    def module(self):
        """Get the module from the current object, kwargs or url."""
        if self.get_context_from_object:
            return self._get_object(Module, 'module')

        if 'module' in self.kwargs \
                and isinstance(self.kwargs['module'], Module):
            return self.kwargs['module']

        if self.module_url_kwarg and self.module_url_kwarg in self.kwargs:
            lookup = {
                self.module_lookup_field: self.kwargs[self.module_url_kwarg]
            }
            return get_object_or_404(Module, **lookup)

    @property
    def project(self):
        """Get the project from the module, kwargs, url or current object."""
        if self.module:
            return self.module.project

        if self.get_context_from_object:
            return self._get_object(Project, 'project')

        if 'project' in self.kwargs \
                and isinstance(self.kwargs['project'], Project):
            return self.kwargs['project']

        if self.project_url_kwarg and self.project_url_kwarg in self.kwargs:
            lookup = {
                self.project_lookup_field: self.kwargs[self.project_url_kwarg]
            }
            return get_object_or_404(Project, **lookup)

    def _get_object(self, cls, attr):
        # CreateView supplies a defect get_object method and has to be excluded
        if hasattr(self, 'get_object') \
                and not isinstance(self, generic.CreateView):
            try:
                object = self.get_object()
                if isinstance(object, cls):
                    return object

                if hasattr(object, attr):
                    return getattr(object, attr)
            except Http404:
                return None
            except AttributeError:
                return None

        return None

    def get_context_data(self, **kwargs):
        """Append project and module to the template context."""
        if 'project' not in kwargs:
            kwargs['project'] = self.project
        if 'module' not in kwargs:
            kwargs['module'] = self.module
        return super(ProjectContextMixin, self).get_context_data(**kwargs)


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

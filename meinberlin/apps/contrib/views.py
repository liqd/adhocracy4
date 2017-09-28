from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views import generic

from adhocracy4.modules.models import Module
from adhocracy4.projects.models import Project


class ProjectContextMixin(generic.base.ContextMixin):
    """Add project and module attributes to the view and the template context.

    This acts as a replacement of ProjectMixin and
    is a counterpart to the PhaseDispatcher logic.
    """

    project_lookup_field = 'slug'
    project_url_kwarg = 'project_slug'
    module_lookup_field = 'slug'
    module_url_kwarg = 'module_slug'

    @property
    def module(self):
        """Get the module from the kwargs, url or current object."""
        if 'module' in self.kwargs \
                and isinstance(self.kwargs['module'], Module):
            return self.kwargs['module']

        if self.module_url_kwarg and self.module_url_kwarg in self.kwargs:
            lookup = {
                self.module_lookup_field: self.kwargs[self.module_url_kwarg]
            }
            return get_object_or_404(Module, **lookup)

        return self._get_object(Module, 'module')

    @property
    def project(self):
        """Get the project from the module, kwargs, url or current object."""
        if self.module:
            return self.module.project

        if 'project' in self.kwargs \
                and isinstance(self.kwargs['project'], Project):
            return self.kwargs['project']

        if self.project_url_kwarg and self.project_url_kwarg in self.kwargs:
            lookup = {
                self.project_lookup_field: self.kwargs[self.project_url_kwarg]
            }
            return get_object_or_404(Project, **lookup)

        return self._get_object(Project, 'project')

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

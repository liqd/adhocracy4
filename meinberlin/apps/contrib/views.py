from django.http import Http404
from django.http import HttpResponseForbidden
from django.http import HttpResponseServerError
from django.shortcuts import get_object_or_404
from django.views import generic

from adhocracy4.modules.models import Module
from adhocracy4.projects.models import Project


class ProjectContextDispatcher(generic.base.ContextMixin, generic.View):
    """Add project and module attributes to the view.

    This acts as a replacement of ProjectMixin and
    is a counterpart to the PhaseDispatcher logic.

    Note: Must always be defined as the _first_ parent class.
    """

    project_lookup_field = 'slug'
    project_url_kwarg = 'project_slug'
    module_lookup_field = 'slug'
    module_url_kwarg = 'module_slug'

    def get_module(self, *args, **kwargs):
        """Get the module from the kwargs, url or current object.

        Note: May be overwritten by views with different module relations.
        """
        if 'module' in kwargs and isinstance(kwargs['module'], Module):
            return kwargs['module']

        if self.module_url_kwarg and self.module_url_kwarg in kwargs:
            lookup = {
                self.module_lookup_field: kwargs[self.module_url_kwarg]
            }
            return get_object_or_404(Module, **lookup)

        return self._get_object(Module, 'module')

    def get_project(self, *args, **kwargs):
        """Get the project from the module, kwargs, url or current object.

        Note: May be overwritten by views with different projects relations.
        """
        if self.module:
            return self.module.project

        if 'project' in kwargs and isinstance(kwargs['project'], Project):
            return kwargs['project']

        if self.project_url_kwarg and self.project_url_kwarg in kwargs:
            lookup = {
                self.project_lookup_field: kwargs[self.project_url_kwarg]
            }
            return get_object_or_404(Project, **lookup)

        return self._get_object(Project, 'project')

    def validate_object_project(self):
        """Validate that the current objects project matches the context."""
        object_project = self._get_object(Project, 'project')
        return not object_project or object_project == self.project

    def validate_object_module(self):
        """Validate that the current objects module matches the context."""
        object_module = self._get_object(Module, 'module')
        return not object_module or object_module == self.module

    def _get_object(self, cls, attr):
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

    def dispatch(self, request, *args, **kwargs):
        """Get this contexts project and module and validate them."""
        module = self.get_module(*args, **kwargs)
        self.module = module
        self.request.module = module

        project = self.get_project(*args, **kwargs)
        self.project = project
        self.request.project = project

        if not project:
            return HttpResponseServerError()

        if not self.validate_object_project()\
                or not self.validate_object_module():
            return HttpResponseForbidden()

        return super(ProjectContextDispatcher, self)\
            .dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Append project to the template context."""
        if 'project' not in kwargs:
            kwargs['project'] = self.project
        if 'module' not in kwargs:
            kwargs['module'] = self.module
        return super(ProjectContextDispatcher, self).get_context_data(**kwargs)

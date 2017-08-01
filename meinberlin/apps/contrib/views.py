from django.http import Http404
from django.http import HttpResponseForbidden
from django.http import HttpResponseServerError
from django.shortcuts import get_object_or_404
from django.views import generic

from adhocracy4.modules.models import Module
from adhocracy4.projects.models import Project


class ProjectContextDispatcher(generic.base.ContextMixin, generic.View):
    """Add a project attribute to the view.

    Note: Must always be defined as the _first_ parent class.
    """

    project_lookup_field = 'slug'
    project_url_kwarg = 'project_slug'
    module_lookup_field = 'slug'
    module_url_kwarg = 'module_slug'

    def get_module(self, *args, **kwargs):
        """Get the module from the kwargs or the url.

        Note: May be overwritten by views with different module relations.
        """
        if 'module' in kwargs and isinstance(kwargs['module'], Module):
            return kwargs['module']

        if self.module_url_kwarg and self.module_url_kwarg in kwargs:
            lookup = {
                self.module_lookup_field: kwargs[self.module_url_kwarg]
            }
            return get_object_or_404(Module, **lookup)

        return None

    def validate_object_module(self):
        """Validate that the current objects module matches the context."""
        object_module = self._get_object_module()
        return not object_module or object_module == self.module

    def _get_object_module(self):
        if hasattr(self, 'get_object') \
                and not isinstance(self, generic.CreateView):
            try:
                object = self.get_object()
                if hasattr(object, 'module'):
                    return object.module

                if isinstance(object, Module):
                    return object
            except Http404:
                return None
            except AttributeError:
                return None

        return None

    def get_project(self, *args, **kwargs):
        """Get the project from the kwargs, the url or the current object.

        Note: May be overwritten by views with different projects relations.
              If a module is detected, the project
        """
        if 'project' in kwargs and isinstance(kwargs['project'], Project):
            return kwargs['project']

        if 'module' in kwargs:
            return kwargs['module'].project

        if self.project_url_kwarg and self.project_url_kwarg in kwargs:
            lookup = {
                self.project_lookup_field: kwargs[self.project_url_kwarg]
            }
            return get_object_or_404(Project, **lookup)

        return self._get_object_project()

    def validate_object_project(self):
        """Validate that the current objects project matches the context."""
        object_project = self._get_object_project()
        return not object_project or object_project == self.project

    def _get_object_project(self):
        if hasattr(self, 'get_object') \
                and not isinstance(self, generic.CreateView):
            try:
                object = self.get_object()
                if hasattr(object, 'project'):
                    return object.project

                if isinstance(object, Project):
                    return object
            except Http404:
                return None
            except AttributeError:
                return None

        return None

    def dispatch(self, request, *args, **kwargs):
        """Get this contexts project and validate it."""
        module = self.get_module(*args, **kwargs)
        if module:
            project = module.project
        else:
            project = self.get_project(*args, **kwargs)
            module = project.last_active_module

        if not project:
            return HttpResponseServerError()

        self.project = project
        self.request.project = project
        self.module = module
        self.request.module = module

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

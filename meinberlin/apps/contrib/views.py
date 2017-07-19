from django.http import Http404
from django.http import HttpResponseForbidden
from django.http import HttpResponseServerError
from django.shortcuts import get_object_or_404
from django.views import generic

from adhocracy4.projects.models import Project


class ProjectContextDispatcher(generic.base.ContextMixin, generic.View):
    """Add a project attribute to the view.

    Note: Must always be defined as the _first_ parent class.
    """

    project_lookup_field = 'slug'
    project_url_kwarg = 'project_slug'

    def get_project(self, *args, **kwargs):
        """Get the project from the kwargs, the url or the current object.

        Note: May be overwritten by views with different projects relations.
        """
        if 'project' in kwargs and isinstance(kwargs['project'], Project):
            return kwargs['project']

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
        if hasattr(self, 'get_object'):
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
        project = self.get_project(*args, **kwargs)
        if not project:
            return HttpResponseServerError()

        self.project = project
        self.request.project = project

        if not self.validate_object_project():
            return HttpResponseForbidden()

        return super(ProjectContextDispatcher, self)\
            .dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Append project to the template context."""
        if 'project' not in kwargs:
            kwargs['project'] = self.project
        return super(ProjectContextDispatcher, self).get_context_data(**kwargs)

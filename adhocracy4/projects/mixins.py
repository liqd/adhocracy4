from django.http import Http404
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.functional import cached_property
from django.views import generic

from adhocracy4.modules.models import Module
from adhocracy4.projects.models import Project


class PhaseDispatchMixin(generic.DetailView):

    @cached_property
    def project(self):
        return self.get_object()

    @cached_property
    def module(self):
        return self.project.last_active_module

    def dispatch(self, request, *args, **kwargs):
        # Choose the appropriate view for the current active phase.
        kwargs['project'] = self.project
        kwargs['module'] = self.module

        return self._view_by_phase()(request, *args, **kwargs)

    def _view_by_phase(self):
        """
        Choose the appropriate view for the current active phase.
        """
        if self.module and self.module.last_active_phase:
            return self.module.last_active_phase.view.as_view()
        else:
            return super().dispatch


class ModuleDispatchMixin(PhaseDispatchMixin):

    @cached_property
    def project(self):
        return self.module.project

    @cached_property
    def module(self):
        return self.get_object()

    def dispatch(self, request, *args, **kwargs):
        # Redirect to the project detail page if the module is shown there
        if self.module == self.project.last_active_module:
            return HttpResponseRedirect(self.project.get_absolute_url())

        return super().dispatch(request, *args, **kwargs)


class ProjectMixin(generic.base.ContextMixin):
    """Add project and module attributes to the view and the template context.

    This is a counterpart to the Phase- / ModuleDispatcher logic.

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
        return super().get_context_data(**kwargs)

from django.db.models import Max
from django.db.models import Min
from django.db.models import Q
from django.http import Http404
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import resolve
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
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


class ModuleClusterMixin:

    def _get_module_dict(self, count, start_date, end_date):
        return {
            'title': _('{}. Online Participation').format(str(count)),
            'type': 'module',
            'count': count,
            'date': start_date,
            'end_date': end_date,
            'modules': []
        }

    def get_module_clusters(self, modules):
        modules = modules\
            .exclude(Q(start_date=None) | Q(end_date=None))
        clusters = []
        try:
            start_date = modules.first().start_date
            end_date = modules.first().end_date
            count = 1
            first_cluster = self._get_module_dict(
                count, start_date, end_date)
            first_cluster['modules'].append(modules.first())
            current_cluster = first_cluster
            clusters.append(first_cluster)

            for module in modules[1:]:
                if module.start_date > end_date:
                    start_date = module.start_date
                    end_date = module.end_date
                    count += 1
                    next_cluster = self._get_module_dict(
                        count, start_date, end_date)
                    next_cluster['modules'].append(module)
                    current_cluster = next_cluster
                    clusters.append(next_cluster)
                else:
                    current_cluster['modules'].append(module)
                    if module.end_date > end_date:
                        end_date = module.end_date
                        current_cluster['end_date'] = end_date
        except AttributeError:
            return clusters
        if len(clusters) == 1:
            clusters[0]['title'] = _('Online Participation')
        return clusters


class DisplayProjectOrModuleMixin(generic.base.ContextMixin,
                                  ModuleClusterMixin):

    @cached_property
    def module_clusters(self):
        return super().get_module_clusters(self.modules)

    @cached_property
    def url_name(self):
        return resolve(self.request.path_info).url_name

    @cached_property
    def modules(self):
        return self.project.modules\
            .annotate(start_date=Min('phase__start_date'))\
            .annotate(end_date=Max('phase__end_date'))\
            .exclude(Q(start_date=None) | Q(end_date=None))\
            .order_by('start_date')

    @cached_property
    def events(self):
        if hasattr(self.project, 'offlineevent_set'):
            return self.project.offlineevent_set.all()
        return []

    @cached_property
    def full_list(self):
        module_cluster = self.module_clusters
        event_list = self.get_events_list()
        full_list = module_cluster + list(event_list)
        return sorted(full_list, key=lambda k: k['date'])

    @cached_property
    def other_modules(self):
        for cluster in self.module_clusters:
            if self.module in cluster['modules']:
                idx = cluster['modules'].index(self.module)
                modules = cluster['modules']
                return modules, idx
        return []

    @cached_property
    def extends(self):
        if self.url_name == 'module-detail':
            return 'a4modules/module_detail.html'
        return 'a4projects/project_detail.html'

    @cached_property
    def display_timeline(self):
        return len(self.full_list) > 1

    @cached_property
    def initial_slide(self):
        initial_slide = self.request.GET.get('initialSlide')
        if initial_slide:
            return int(initial_slide)
        else:
            now = timezone.now()
            for idx, val in enumerate(self.full_list):
                if 'type' in val and val['type'] == 'module':
                    start_date = val['date']
                    end_date = val['end_date']
                    if start_date and end_date:
                        if now >= start_date and now <= end_date:
                            return idx
            for idx, val in enumerate(self.full_list):
                if 'type' not in val:
                    date = val['date']
                    if date:
                        if now <= date:
                            return idx
        return 0

    def get_current_event(self):
        fl = self.full_list
        idx = self.initial_slide
        try:
            current_dict = fl[idx]
            if 'type' not in current_dict:
                return self.full_list[self.initial_slide]
        except (IndexError, KeyError):
            return []
        return []

    def get_current_modules(self):
        fl = self.full_list
        idx = self.initial_slide
        try:
            current_dict = fl[idx]
            if current_dict['type'] == 'module':
                return self.full_list[self.initial_slide]['modules']
        except (IndexError, KeyError):
            return []

    def get_events_list(self):
        return self.events.values('date', 'name',
                                  'event_type',
                                  'slug', 'description')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_name'] = self.url_name
        context['extends'] = self.extends
        if self.url_name == 'module-detail':
            cluster, idx = self.other_modules
            next_module = None
            previous_module = None
            try:
                next_module = cluster[idx + 1]
            except IndexError:
                pass
            try:
                if idx > 0:
                    previous_module = cluster[idx - 1]
            except IndexError:
                pass
            context['other_modules'] = cluster
            context['index'] = idx + 1
            context['next'] = next_module
            context['previous'] = previous_module
        else:
            context['event'] = self.get_current_event()
            context['modules'] = self.get_current_modules()
            context['participation_dates'] = self.full_list
            context['initial_slide'] = self.initial_slide
        return context

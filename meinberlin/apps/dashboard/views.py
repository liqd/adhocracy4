from django.apps import apps
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.urls import resolve
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.views import generic
from django.views.generic.detail import SingleObjectMixin

from adhocracy4.dashboard import mixins
from adhocracy4.dashboard import signals
from adhocracy4.dashboard import views as a4dashboard_views
from adhocracy4.dashboard.blueprints import get_blueprints
from adhocracy4.modules import models as module_models
from adhocracy4.phases import models as phase_models
from adhocracy4.projects import models as project_models
from adhocracy4.projects.mixins import ProjectMixin
from meinberlin.apps.dashboard.forms import DashboardProjectCreateForm


class ModuleBlueprintListView(ProjectMixin,
                              mixins.DashboardBaseMixin,
                              generic.DetailView):
    template_name = 'meinberlin_dashboard/module_blueprint_list.html'
    permission_required = 'a4projects.add_project'
    model = project_models.Project
    slug_url_kwarg = 'project_slug'
    menu_item = 'project'

    @property
    def blueprints(self):
        return [
            (key, data) for key, data in get_blueprints()
            if key not in ['bplan', 'external-project']
        ]

    def get_permission_object(self):
        return self.organisation


class ModuleCreateView(ProjectMixin,
                       mixins.DashboardBaseMixin,
                       mixins.BlueprintMixin,
                       SingleObjectMixin,
                       generic.View):
    permission_required = 'a4projects.add_project'
    model = project_models.Project
    slug_url_kwarg = 'project_slug'

    def post(self, request, *args, **kwargs):
        project = self.get_object()
        weight = 1
        if project.modules:
            weight = max(
                project.modules.values_list('weight', flat=True)
            ) + 1
        module = module_models.Module(
            name=self.blueprint.title,
            weight=weight,
            project=project,
            is_draft=True,
        )
        module.save()
        signals.module_created.send(sender=None,
                                    module=module,
                                    user=self.request.user)

        self._create_module_settings(module)
        self._create_phases(module, self.blueprint.content)

        return HttpResponseRedirect(self.get_next(module))

    def _create_module_settings(self, module):
        if self.blueprint.settings_model:
            settings_model = apps.get_model(*self.blueprint.settings_model)
            module_settings = settings_model(module=module)
            module_settings.save()

    def _create_phases(self, module, blueprint_phases):
        for index, phase_content in enumerate(blueprint_phases):
            phase = phase_models.Phase(
                type=phase_content.identifier,
                name=phase_content.name,
                description=phase_content.description,
                weight=index,
                module=module,
            )
            phase.save()

    def get_next(self, module):
        return reverse('a4dashboard:dashboard-module_basic-edit', kwargs={
            'module_slug': module.slug
        })

    def get_permission_object(self):
        return self.organisation


class ModulePublishView(SingleObjectMixin,
                        generic.View):
    permission_required = 'a4projects.change_project'
    model = module_models.Module
    slug_url_kwarg = 'module_slug'

    def get_permission_object(self):
        return self.get_object().project

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action', None)
        if action == 'publish':
            self.publish_module()
        elif action == 'unpublish':
            self.unpublish_module()
        else:
            messages.warning(self.request, _('Invalid action'))

        return HttpResponseRedirect(self.get_next())

    def get_next(self):
        if 'referrer' in self.request.POST:
            return self.request.POST['referrer']
        elif 'HTTP_REFERER' in self.request.META:
            return self.request.META['HTTP_REFERER']

        return reverse('a4dashboard:project-edit', kwargs={
            'project_slug': self.project.slug
        })

    def publish_module(self):
        module = self.get_object()
        if not module.is_draft:
            messages.info(self.request, _('Module is already added'))
            return

        module.is_draft = False
        module.save()

        signals.module_published.send(sender=None,
                                      module=module,
                                      user=self.request.user)

        messages.success(self.request,
                         _('Module successfully added.'))

    def unpublish_module(self):
        module = self.get_object()
        if module.is_draft:
            messages.info(self.request, _('Module is already removed'))
            return

        module.is_draft = True
        module.save()

        signals.module_unpublished.send(sender=None,
                                        module=module,
                                        user=self.request.user)

        messages.success(self.request,
                         _('Module successfully removed.'))


class ModuleDeleteView(generic.DeleteView):
    permission_required = 'a4projects.change_project'
    model = module_models.Module
    success_message = _('The module has been deleted')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)

    def get_permission_object(self):
        return self.get_object().project

    def get_success_url(self):
        referrer = self.request.POST.get('referrer', None) \
            or self.request.META.get('HTTP_REFERER', None)
        if referrer:
            view, args, kwargs = resolve(referrer)
            if 'module_slug' not in kwargs \
                    or not kwargs['module_slug'] == self.get_object().slug:
                return referrer

        return reverse('a4dashboard:project-edit', kwargs={
            'project_slug': self.get_object().project.slug
        })


class DashboardProjectListView(a4dashboard_views.ProjectListView):
    def get_queryset(self):
        return super().get_queryset().filter(projectcontainer=None)


class ProjectCreateView(mixins.DashboardBaseMixin,
                        SuccessMessageMixin,
                        generic.CreateView):
    model = project_models.Project
    slug_url_kwarg = 'project_slug'
    form_class = DashboardProjectCreateForm
    template_name = 'a4dashboard/project_create_form.html'
    permission_required = 'a4projects.add_project'
    menu_item = 'project'
    success_message = _('Project successfully created.')

    def get_permission_object(self):
        return self.organisation

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['organisation'] = self.organisation
        kwargs['creator'] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse('a4dashboard:project-edit',
                       kwargs={'project_slug': self.object.slug})

    def form_valid(self, form):
        response = super().form_valid(form)
        signals.project_created.send(sender=None,
                                     project=self.object,
                                     user=self.request.user)

        return response

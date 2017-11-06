from django.apps import apps
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django.views import generic
from django.views.generic.detail import SingleObjectMixin

from adhocracy4.modules import models as module_models
from adhocracy4.phases import models as phase_models
from adhocracy4.projects import models as project_models
from meinberlin.apps.contrib.views import ProjectContextMixin
from meinberlin.apps.dashboard2 import mixins as a4dashboard_mixins
from meinberlin.apps.dashboard2 import views as a4dashboard_views
from meinberlin.apps.dashboard2.blueprints import get_blueprints
from meinberlin.apps.newsletters.forms import NewsletterForm
from meinberlin.apps.newsletters.views import NewsletterCreateView
from meinberlin.apps.organisations.models import Organisation
from meinberlin.apps.plans.forms import PlanForm
from meinberlin.apps.plans.models import Plan

from . import forms


class DashboardProjectListView(a4dashboard_views.ProjectListView):
    def get_queryset(self):
        return super().get_queryset().filter(projectcontainer=None)


class DashboardOrganisationUpdateView(a4dashboard_mixins.DashboardBaseMixin,
                                      SuccessMessageMixin,
                                      generic.UpdateView):

    model = Organisation
    form_class = forms.OrganisationForm
    slug_url_kwarg = 'organisation_slug'
    template_name = 'meinberlin_dashboard/organisation_form.html'
    success_message = _('Organisation successfully updated.')
    permission_required = 'meinberlin_organisations.change_organisation'
    menu_item = 'organisation'

    def get_permission_object(self):
        return self.organisation


class DashboardNewsletterCreateView(a4dashboard_mixins.DashboardBaseMixin,
                                    NewsletterCreateView):
    template_name = 'meinberlin_dashboard/newsletter_form.html'
    menu_item = 'newsletter'
    form_class = NewsletterForm
    permission_required = 'a4projects.add_project'

    def get_email_kwargs(self):
        kwargs = {}
        kwargs.update({'organisation_pk': self.organisation.pk})
        return kwargs

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['organisation'] = self.organisation
        kwargs.pop('user')
        return kwargs

    def get_success_url(self):
        return reverse(
            'a4dashboard:newsletter-create',
            kwargs={'organisation_slug': self.organisation.slug})

    def get_permission_object(self):
        return self.organisation


class ModuleBlueprintListView(ProjectContextMixin,
                              a4dashboard_mixins.DashboardBaseMixin,
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


class ModuleCreateView(ProjectContextMixin,
                       a4dashboard_mixins.DashboardBaseMixin,
                       a4dashboard_mixins.BlueprintMixin,
                       SingleObjectMixin,
                       generic.View):
    permission_required = 'a4projects.add_project'
    model = project_models.Project
    slug_url_kwarg = 'project_slug'

    def post(self, request, *args, **kwargs):
        project = self.get_object()
        module = module_models.Module(
            name=self.blueprint.title,
            weight=len(project.modules) + 1,
            project=project,
        )
        module.save()

        self._create_module_settings(module)
        self._create_phases(module, self.blueprint.content)

        return HttpResponseRedirect(self.get_next(module))

    def _create_module_settings(self, module):
        if self.blueprint.settings_model:
            settings_model = apps.get_model(*self.blueprint.settings_model)
            module_settings = settings_model(module=module)
            module_settings.save()

    def _create_phases(self, module, blueprint_phases):
        for phase_content in blueprint_phases:
            phase = phase_models.Phase(
                type=phase_content.identifier,
                name=phase_content.name,
                description=phase_content.description,
                weight=phase_content.weight,
                module=module,
            )
            phase.save()

    def get_next(self, module):
        return reverse('a4dashboard:dashboard-module_basic-edit', kwargs={
            'module_slug': module.slug
        })

    def get_permission_object(self):
        return self.organisation


class PlanListView(a4dashboard_mixins.DashboardBaseMixin,
                   generic.ListView):
    model = Plan
    template_name = 'meinberlin_dashboard/plan_list.html'
    permission_required = 'a4projects.add_project'
    menu_item = 'project'

    def get_permission_object(self):
        return self.organisation

    def get_queryset(self):
        return super().get_queryset().filter(organisation=self.organisation)


class PlanCreateView(a4dashboard_mixins.DashboardBaseMixin,
                     generic.CreateView):
    model = Plan
    form_class = PlanForm
    permission_required = 'meinberlin_plans.add_plan'
    template_name = 'meinberlin_dashboard/plan_create_form.html'
    menu_item = 'project'

    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.instance.organisation = self.organisation
        return super().form_valid(form)

    def get_permission_object(self):
        return self.organisation

    def get_success_url(self):
        return reverse(
            'a4dashboard:plan-list',
            kwargs={'organisation_slug': self.organisation.slug})


class PlanUpdateView(a4dashboard_mixins.DashboardBaseMixin,
                     generic.UpdateView):
    model = Plan
    form_class = PlanForm
    permission_required = 'meinberlin_plans.add_plan'
    template_name = 'meinberlin_dashboard/plan_update_form.html'
    menu_item = 'project'

    def get_permission_object(self):
        return self.organisation

    def get_success_url(self):
        return reverse(
            'a4dashboard:plan-list',
            kwargs={'organisation_slug': self.organisation.slug})


class PlanDeleteView(a4dashboard_mixins.DashboardBaseMixin,
                     generic.DeleteView):
    model = Plan
    success_message = _('The plan has been deleted')
    permission_required = 'meinberlin_plans.change_plan'
    template_name = 'meinberlin_dashboard/plan_confirm_delete.html'
    menu_item = 'project'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)

    def get_permission_object(self):
        return self.organisation

    def get_success_url(self):
        return reverse(
            'a4dashboard:plan-list',
            kwargs={'organisation_slug': self.organisation.slug})

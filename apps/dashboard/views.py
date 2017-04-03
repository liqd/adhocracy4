from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.utils import functional
from django.utils.translation import ugettext as _
from django.views import generic
from rules.compat import access_mixins as mixins

from adhocracy4.categories import models as category_models
from adhocracy4.phases import models as phase_models
from adhocracy4.projects import models as project_models
from adhocracy4.rules import mixins as rules_mixins

from apps.organisations.models import Organisation

from . import blueprints
from . import forms


class DashboardBaseMixin(mixins.LoginRequiredMixin,
                         generic.base.ContextMixin):

    @functional.cached_property
    def organisation(self):
        if 'organisation_slug' in self.kwargs:
            slug = self.kwargs['organisation_slug']
            return get_object_or_404(Organisation, slug=slug)
        else:
            return self.request.user.organisation_set.first()

    @functional.cached_property
    def other_organisations_of_user(self):
        user = self.request.user
        if self.organisation:
            return user.organisation_set.exclude(pk=self.organisation.pk)
        else:
            return None

    def get_permission_object(self):
        return self.organisation


class DashboardProjectListView(DashboardBaseMixin,
                               rules_mixins.PermissionRequiredMixin,
                               generic.ListView):
    model = project_models.Project
    template_name = 'meinberlin_dashboard/project_list.html'
    permission_required = 'meinberlin_organisations.initiate_project'

    def get_queryset(self):
        return self.model.objects.filter(
            organisation=self.organisation
        )

    def get_success_url(self):
        return reverse('dashboard-project-list')


class DashboardBlueprintListView(DashboardBaseMixin,
                                 rules_mixins.PermissionRequiredMixin,
                                 generic.TemplateView):
    template_name = 'meinberlin_dashboard/blueprint_list.html'
    blueprints = blueprints.blueprints
    permission_required = 'meinberlin_organisations.initiate_project'


class DashboardProjectCreateView(DashboardBaseMixin,
                                 rules_mixins.PermissionRequiredMixin,
                                 SuccessMessageMixin,
                                 blueprints.BlueprintMixin,
                                 generic.CreateView):
    model = project_models.Project
    form_class = forms.ProjectCreateForm
    template_name = 'meinberlin_dashboard/project_create_form.html'
    success_message = _('Project succesfully created.')
    permission_required = 'meinberlin_organisations.initiate_project'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['blueprint'] = self.blueprint
        kwargs['organisation'] = self.organisation
        kwargs['creator'] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse(
            'dashboard-project-list',
            kwargs={'organisation_slug': self.organisation.slug, })


class DashboardProjectUpdateView(DashboardBaseMixin,
                                 rules_mixins.PermissionRequiredMixin,
                                 SuccessMessageMixin,
                                 generic.UpdateView):
    model = project_models.Project
    form_class = forms.ProjectUpdateForm
    template_name = 'meinberlin_dashboard/project_update_form.html'
    success_message = _('Project successfully updated.')
    permission_required = 'meinberlin_organisations.initiate_project'

    def get_success_url(self):
        return reverse('dashboard-project-list',
                       kwargs={
                           'organisation_slug': self.organisation.slug,
                       })

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        qs = phase_models.Phase.objects.filter(module__project=self.object)
        kwargs['phases__queryset'] = qs

        if qs.first().module.settings_instance:
            settings_instance = qs.first().module.settings_instance
            kwargs['module_settings__instance'] = settings_instance

        kwargs['categories__queryset'] = \
            category_models.Category.objects.filter(
                module__project=self.object)

        return kwargs


class DashboardProjectModeratorsView(DashboardBaseMixin,
                                     rules_mixins.PermissionRequiredMixin,
                                     SuccessMessageMixin,
                                     generic.UpdateView):

    model = project_models.Project
    form_class = forms.AddModeratorForm
    template_name = 'meinberlin_dashboard/project_moderators.html'
    success_message = _('Moderators successfully updated.')
    permission_required = 'meinberlin_organisations.initiate_project'

    def get_permission_object(self):
        return self.organisation

    def get_success_url(self):
        return self.request.path

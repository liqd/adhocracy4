from allauth.account import views as account_views
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _
from django.views import generic

from adhocracy4.categories import models as category_models
from adhocracy4.phases import models as phase_models
from adhocracy4.projects import models as project_models
from adhocracy4.rules import mixins as rules_mixins

from apps.users.models import User

from . import mixins as dashboard_mixins
from . import blueprints
from . import forms


class DashboardProjectListView(dashboard_mixins.DashboardBaseMixin,
                               rules_mixins.PermissionRequiredMixin,
                               dashboard_mixins.DashboardProjectPublishMixin,
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


class DashboardBlueprintListView(dashboard_mixins.DashboardBaseMixin,
                                 rules_mixins.PermissionRequiredMixin,
                                 generic.TemplateView):
    template_name = 'meinberlin_dashboard/blueprint_list.html'
    blueprints = blueprints.blueprints
    permission_required = 'meinberlin_organisations.initiate_project'


class DashboardProjectCreateView(dashboard_mixins.DashboardBaseMixin,
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


class DashboardProjectUpdateView(dashboard_mixins.DashboardBaseMixin,
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


class DashboardEmailView(dashboard_mixins.DashboardBaseMixin,
                         account_views.EmailView):
    menu_item = 'email'
    template_name = 'meinberlin_dashboard/email.html'

    def get_success_url(self):
        return self.request.path


class DashboardProfileView(dashboard_mixins.DashboardBaseMixin,
                           SuccessMessageMixin,
                           generic.UpdateView):

    model = User
    template_name = "meinberlin_dashboard/profile.html"
    form_class = forms.ProfileForm
    success_message = _("Your profile was successfully updated.")
    menu_item = 'profile'

    def get_object(self):
        return get_object_or_404(User, pk=self.request.user.id)

    def get_success_url(self):
        return self.request.path


class ChangePasswordView(dashboard_mixins.DashboardBaseMixin,
                         account_views.PasswordChangeView):
    menu_item = 'password'
    template_name = 'meinberlin_dashboard/password.html'

    def get_success_url(self):
        return reverse('dashboard-password')

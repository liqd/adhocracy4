from django.apps import apps
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django.views import generic
from django.views.generic.detail import SingleObjectMixin

from adhocracy4.modules import models as module_models
from adhocracy4.phases import models as phase_models
from adhocracy4.projects import models as project_models
from meinberlin.apps.dashboard2 import mixins as a4dashboard_mixins
from meinberlin.apps.dashboard2 import views as a4dashboard_views
from meinberlin.apps.dashboard2.blueprints import get_blueprints
from meinberlin.apps.newsletters.forms import NewsletterForm
from meinberlin.apps.newsletters.views import NewsletterCreateView
from meinberlin.apps.organisations.models import Organisation

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


class ModuleCreateView(a4dashboard_mixins.DashboardBaseMixin,
                       a4dashboard_mixins.BlueprintMixin,
                       SingleObjectMixin,
                       generic.View):
    permission_required = 'a4projects.add_project'
    model = project_models.Project
    slug_url_kwarg = 'project_slug'

    def post(self, request, *args, **kwargs):
        project = self.get_object()
        module = module_models.Module(
            name='Onlinebeteiligung',
            description=project.description,
            weight=1,
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

from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.views import generic

from meinberlin.apps.bplan import models as bplan_models
from meinberlin.apps.dashboard2 import mixins as a4dashboard_mixins
from meinberlin.apps.dashboard2.components.forms.views import \
    ProjectComponentFormView
from meinberlin.apps.extprojects.views import ExternalProjectCreateView
from meinberlin.apps.newsletters.forms import NewsletterForm
from meinberlin.apps.newsletters.views import NewsletterCreateView
from meinberlin.apps.organisations.models import Organisation

from . import forms


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


class BplanProjectCreateView(ExternalProjectCreateView):

    model = bplan_models.Bplan
    slug_url_kwarg = 'project_slug'
    blueprint_key = 'bplan'
    form_class = forms.BplanProjectCreateForm
    template_name = 'meinberlin_dashboard/external_project_create_form.html'


class BplanProjectUpdateView(ProjectComponentFormView):

    model = bplan_models.Bplan

    def get_project(self, *args, **kwargs):
        project = super().get_project(*args, **kwargs)
        return project.externalproject.bplan

    def get_object(self, queryset=None):
        return self.project

    def validate_object_project(self):
        return True

    def validate_object_module(self):
        return True

from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.views import generic

from adhocracy4.rules import mixins as rules_mixins
from meinberlin.apps.newsletters.forms import NewsletterForm
from meinberlin.apps.newsletters.views import NewsletterCreateView
from meinberlin.apps.organisations.models import Organisation

from . import forms
from . import mixins


class DashboardOrganisationUpdateView(mixins.DashboardBaseMixin,
                                      rules_mixins.PermissionRequiredMixin,
                                      SuccessMessageMixin,
                                      generic.UpdateView):

    model = Organisation
    form_class = forms.OrganisationForm
    slug_url_kwarg = 'organisation_slug'
    template_name = 'meinberlin_dashboard/organisation_form.html'
    success_message = _('Organisation successfully updated.')
    permission_required = 'meinberlin_organisations.change_organisation'
    menu_item = 'organisation'


class DashboardNewsletterCreateView(mixins.DashboardBaseMixin,
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
            'dashboard-newsletter-create',
            kwargs={'organisation_slug': self.organisation.slug})

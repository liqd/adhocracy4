from django.core.urlresolvers import reverse

from meinberlin.apps.dashboard2 import mixins as a4dashboard_mixins
from meinberlin.apps.dashboard2 import views as a4dashboard_views
from meinberlin.apps.newsletters.forms import NewsletterForm
from meinberlin.apps.newsletters.views import NewsletterCreateView


class DashboardProjectListView(a4dashboard_views.ProjectListView):
    def get_queryset(self):
        return super().get_queryset().filter(projectcontainer=None)


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

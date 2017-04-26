from django.core.urlresolvers import reverse
from django.views import generic

from adhocracy4.projects import mixins as project_mixins
from adhocracy4.rules import mixins as rules_mixins

from apps.dashboard.mixins import DashboardBaseMixin

from . import forms
from . import models


class PollDetailView(project_mixins.ProjectMixin,
                     rules_mixins.PermissionRequiredMixin,
                     generic.DetailView):
    model = models.Poll
    permission_required = 'meinberlin_polls.view_poll'

    def get_object(self):
        return models.Poll.objects.filter(module=self.module).first()


class PollManagementView(DashboardBaseMixin,
                         rules_mixins.PermissionRequiredMixin,
                         generic.FormView):
    template_name = 'meinberlin_polls/poll_management_form.html'
    form_class = forms.PollForm
    permission_required = 'meinberlin_polls.create_poll'

    # Dashboard related attributes
    menu_item = 'project'

    def get_success_url(self):
        return reverse(
            'dashboard-project-list',
            kwargs={'organisation_slug': self.organisation.slug, })

    def dispatch(self, *args, **kwargs):
        self.project = kwargs['project']
        self.module = self.project.module_set.first()
        self.request.module = self.module
        return super(PollManagementView, self).dispatch(*args, **kwargs)

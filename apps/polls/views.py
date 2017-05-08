from django.core.urlresolvers import reverse
from django.views import generic

from adhocracy4.projects import mixins as project_mixins
from adhocracy4.rules import mixins as rules_mixins

from apps.dashboard.mixins import DashboardBaseMixin

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
                         generic.DetailView):
    template_name = 'meinberlin_polls/poll_management_form.html'
    model = models.Poll
    permission_required = 'a4projects.add_project'

    # Dashboard related attributes
    menu_item = 'project'

    def get_object(self):
        return self.get_or_create_poll()

    def get_or_create_poll(self):
        try:
            obj = models.Poll.objects.get(module=self.module)
        except models.Poll.DoesNotExist:
            obj = models.Poll(module=self.module, creator=self.request.user)
            obj.save()
        return obj

    def get_success_url(self):
        return reverse(
            'dashboard-project-list',
            kwargs={'organisation_slug': self.organisation.slug, })

    def dispatch(self, *args, **kwargs):
        self.project = kwargs['project']
        self.module = self.project.module_set.first()
        self.request.module = self.module
        self.poll = self.get_or_create_poll()

        return super(PollManagementView, self).dispatch(*args, **kwargs)

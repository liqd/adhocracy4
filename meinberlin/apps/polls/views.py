from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.views import generic

from adhocracy4.rules import mixins as rules_mixins
from meinberlin.apps.contrib.views import ProjectContextDispatcher
from meinberlin.apps.dashboard.mixins import DashboardBaseMixin

from . import models


class PollDetailView(ProjectContextDispatcher,
                     rules_mixins.PermissionRequiredMixin,
                     generic.DetailView):
    model = models.Poll
    permission_required = 'meinberlin_polls.view_poll'

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)

        except Http404:
            self.object = None
            context = self.get_context_data(object=None, request=self.request,)
            return render_to_response(
                'meinberlin_polls/poll_404.html',
                context=context,
                status=404
            )

    def get_object(self):
        return get_object_or_404(models.Poll,
                                 module=self.project.last_active_module)

    def get_permission_object(self):
        return self.project.last_active_module


class PollManagementView(ProjectContextDispatcher,
                         DashboardBaseMixin,
                         rules_mixins.PermissionRequiredMixin,
                         generic.DetailView):
    template_name = 'meinberlin_polls/poll_management_form.html'
    model = models.Poll
    permission_required = 'a4projects.add_project'
    project_url_kwarg = 'slug'

    # Dashboard related attributes
    menu_item = 'project'

    def get_object(self):
        return self.get_or_create_poll()

    def get_or_create_poll(self):
        # FIXME: Add multi-module support
        module = self.project.module_set.first()
        try:
            obj = models.Poll.objects.get(module=module)
        except models.Poll.DoesNotExist:
            obj = models.Poll(module=module,
                              creator=self.request.user)
            obj.save()
        return obj

    def get_success_url(self):
        return reverse(
            'dashboard-project-list',
            kwargs={'organisation_slug': self.organisation.slug, })

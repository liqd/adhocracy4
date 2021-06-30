from django.http import Http404
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.views import generic

from adhocracy4.dashboard import mixins as dashboard_mixins
from adhocracy4.projects.mixins import DisplayProjectOrModuleMixin
from adhocracy4.projects.mixins import ProjectMixin
from adhocracy4.rules import mixins as rules_mixins

from . import models


class PollDetailView(ProjectMixin,
                     rules_mixins.PermissionRequiredMixin,
                     generic.DetailView,
                     DisplayProjectOrModuleMixin):
    model = models.Poll
    permission_required = 'a4polls.view_poll'

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)

        except Http404:
            self.object = None
            context = self.get_context_data(object=None, request=self.request,)
            return render_to_response(
                'a4polls/poll_404.html',
                context=context,
                status=404
            )

    def get_object(self):
        return get_object_or_404(models.Poll, module=self.module)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object is not None:
            context['question_list'] = \
                self.object.questions.annotate_vote_count().all()
            context['poll'] = self.get_object()
        return context

    def get_permission_object(self):
        return self.module

    @property
    def phase(self):
        try:
            weight = self.request.GET.get('phase')
            phase = self.project.phases.filter(weight=weight).first()
        except ValueError:
            phase = None

        if phase:
            return phase
        else:
            return self.project.last_active_phase


class PollDashboardView(ProjectMixin,
                        dashboard_mixins.DashboardBaseMixin,
                        dashboard_mixins.DashboardComponentMixin,
                        generic.TemplateView):
    template_name = 'a4polls/poll_dashboard.html'
    permission_required = 'a4projects.change_project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['poll'] = self.get_or_create_poll()
        return context

    def get_or_create_poll(self):
        try:
            obj = models.Poll.objects.get(module=self.module)
        except models.Poll.DoesNotExist:
            obj = models.Poll(module=self.module,
                              creator=self.request.user)
            obj.save()
        return obj

    def get_permission_object(self):
        return self.project

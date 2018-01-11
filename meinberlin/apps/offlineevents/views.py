from django.contrib import messages
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.views import generic

from adhocracy4.projects.mixins import ProjectMixin
from meinberlin.apps.dashboard2 import mixins
from meinberlin.apps.ideas import views as idea_views

from . import forms
from . import models


class OfflineEventDetailView(idea_views.AbstractIdeaDetailView):
    model = models.OfflineEvent
    permission_required = 'meinberlin_offlineevents.view_offlineevent'


class OfflineEventListView(ProjectMixin,
                           mixins.DashboardBaseMixin,
                           mixins.DashboardComponentMixin,
                           generic.ListView):
    model = models.OfflineEvent
    template_name = 'meinberlin_offlineevents/offlineevent_list.html'
    permission_required = 'meinberlin_offlineevents.list_offlineevent'

    def get_queryset(self):
        return super().get_queryset().filter(project=self.project)

    def get_permission_object(self):
        return self.project


class OfflineEventCreateView(ProjectMixin,
                             mixins.DashboardBaseMixin,
                             mixins.DashboardComponentMixin,
                             mixins.DashboardComponentFormSignalMixin,
                             generic.CreateView):
    model = models.OfflineEvent
    form_class = forms.OfflineEventForm
    permission_required = 'meinberlin_offlineevents.add_offlineevent'
    template_name = 'meinberlin_offlineevents/offlineevent_create_form.html'

    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.instance.project = self.project
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'a4dashboard:offlineevent-list',
            kwargs={'project_slug': self.project.slug})

    def get_permission_object(self):
        return self.project


class OfflineEventUpdateView(ProjectMixin,
                             mixins.DashboardBaseMixin,
                             mixins.DashboardComponentMixin,
                             mixins.DashboardComponentFormSignalMixin,
                             generic.UpdateView):
    model = models.OfflineEvent
    form_class = forms.OfflineEventForm
    permission_required = 'meinberlin_offlineevents.change_offlineevent'
    template_name = 'meinberlin_offlineevents/offlineevent_update_form.html'
    get_context_from_object = True

    def get_success_url(self):
        return reverse(
            'a4dashboard:offlineevent-list',
            kwargs={'project_slug': self.project.slug})

    @property
    def organisation(self):
        return self.project.organisation

    def get_permission_object(self):
        return self.project


class OfflineEventDeleteView(ProjectMixin,
                             mixins.DashboardBaseMixin,
                             mixins.DashboardComponentMixin,
                             mixins.DashboardComponentDeleteSignalMixin,
                             generic.DeleteView):
    model = models.OfflineEvent
    success_message = _('The offline event has been deleted')
    permission_required = 'meinberlin_offlineevents.change_offlineevent'
    template_name = 'meinberlin_offlineevents/offlineevent_confirm_delete.html'
    get_context_from_object = True

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse(
            'a4dashboard:offlineevent-list',
            kwargs={'project_slug': self.project.slug})

    @property
    def organisation(self):
        return self.project.organisation

    def get_permission_object(self):
        return self.project

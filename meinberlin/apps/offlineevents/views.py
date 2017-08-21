from django.contrib import messages
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.views import generic

from meinberlin.apps.dashboard2 import mixins
from meinberlin.apps.ideas import views as idea_views

from . import forms
from . import models


class OfflineEventDetailView(idea_views.AbstractIdeaDetailView):
    model = models.OfflineEvent
    permission_required = 'meinberlin_offlineevents.view_offlineevent'


class OfflineEventListView(mixins.DashboardComponentMixin,
                           mixins.DashboardBaseMixin,
                           mixins.DashboardContextMixin,
                           generic.ListView):
    model = models.OfflineEvent
    template_name = 'meinberlin_offlineevents/offlineevent_list.html'
    permission_required = 'meinberlin_offlineevents.list_offlineevent'
    menu_item = 'project'

    def get_queryset(self):
        return super().get_queryset().filter(project=self.project)


class OfflineEventCreateView(mixins.DashboardComponentMixin,
                             mixins.DashboardBaseMixin,
                             mixins.DashboardContextMixin,
                             generic.CreateView):
    model = models.OfflineEvent
    form_class = forms.OfflineEventForm
    permission_required = 'meinberlin_offlineevents.add_offlineevent'
    template_name = 'meinberlin_offlineevents/offlineevent_create_form.html'
    menu_item = 'project'

    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.instance.project = self.project
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'a4dashboard:offlineevent-list',
            kwargs={'project_slug': self.project.slug})


class OfflineEventUpdateView(mixins.DashboardComponentMixin,
                             mixins.DashboardBaseMixin,
                             mixins.DashboardContextMixin,
                             generic.UpdateView):
    model = models.OfflineEvent
    form_class = forms.OfflineEventForm
    permission_required = 'meinberlin_offlineevents.change_offlineevent'
    template_name = 'meinberlin_offlineevents/offlineevent_update_form.html'
    menu_item = 'project'

    def get_success_url(self):
        return reverse(
            'a4dashboard:offlineevent-list',
            kwargs={'project_slug': self.project.slug})

    @property
    def organisation(self):
        return self.project.organisation


class OfflineEventDeleteView(mixins.DashboardComponentMixin,
                             mixins.DashboardBaseMixin,
                             mixins.DashboardContextMixin,
                             generic.DeleteView):
    model = models.OfflineEvent
    success_message = _('The offline event has been deleted')
    permission_required = 'meinberlin_offlineevents.change_offlineevent'
    template_name = 'meinberlin_offlineevents/offlineevent_confirm_delete.html'
    menu_item = 'project'

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

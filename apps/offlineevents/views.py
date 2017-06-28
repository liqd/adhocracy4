from django.contrib import messages
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.views import generic

from adhocracy4.modules import views as module_views
from adhocracy4.projects.models import Project
from adhocracy4.rules import mixins as rules_mixins
from apps.dashboard.mixins import DashboardBaseMixin

from . import forms
from . import models


class OfflineEventDetailView(module_views.ItemDetailView):
    model = models.OfflineEvent
    permission_required = 'meinberlin_offlineevents.view_offlineevent'

    @property
    def project(self):
        return self.get_object().project


class OfflineEventMgmtView(DashboardBaseMixin,
                           rules_mixins.PermissionRequiredMixin,
                           generic.ListView):
    model = models.OfflineEvent
    template_name = 'meinberlin_offlineevents/offlineevent_mgmt_list.html'
    permission_required = 'a4projects.add_project'
    menu_item = 'project'

    def dispatch(self, *args, **kwargs):
        self.project = Project.objects.get(slug=kwargs['slug'])
        return super(OfflineEventMgmtView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        return super().get_queryset().filter(project__slug=self.project)


class OfflineEventMgmtCreateView(rules_mixins.PermissionRequiredMixin,
                                 generic.CreateView):

    model = models.OfflineEvent
    form_class = forms.OfflineEventForm
    permission_required = 'meinberlin_offlineevents.add_offlineevent'
    template_name = \
        'meinberlin_offlineevents/offlineevent_mgmt_create_form.html'
    menu_item = 'project'

    @property
    def organisation(self):
        return self.project.organisation

    def get_permission_object(self):
        return self.organisation

    def dispatch(self, *args, **kwargs):
        self.project = Project.objects.get(slug=kwargs['slug'])
        return super(OfflineEventMgmtCreateView, self).dispatch(
            *args, **kwargs)

    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.instance.project = self.project
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'meinberlin_offlineevents:offlineevent-mgmt',
            kwargs={'slug': self.project.slug})


class OfflineEventMgmtUpdateView(rules_mixins.PermissionRequiredMixin,
                                 generic.UpdateView):
    model = models.OfflineEvent
    form_class = forms.OfflineEventForm
    permission_required = 'meinberlin_offlineevents.change_offlineevent'
    template_name = \
        'meinberlin_offlineevents/offlineevent_mgmt_update_form.html'
    menu_item = 'project'

    @property
    def project(self):
        return self.get_object().project

    @property
    def organisation(self):
        return self.project.organisation

    def get_success_url(self):
        return reverse(
            'meinberlin_offlineevents:offlineevent-mgmt',
            kwargs={'slug': self.project.slug})


class OfflineEventMgmtDeleteView(rules_mixins.PermissionRequiredMixin,
                                 generic.DeleteView):
    model = models.OfflineEvent
    success_message = _('The offline event has been deleted')
    permission_required = 'meinberlin_offlineevents.change_offlineevent'
    template_name = \
        'meinberlin_offlineevents/offlineevent_mgmt_confirm_delete.html'
    menu_item = 'project'

    @property
    def project(self):
        return self.get_object().project

    @property
    def organisation(self):
        return self.get_object().project.organisation

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse(
            'meinberlin_offlineevents:offlineevent-mgmt',
            kwargs={'slug': self.project.slug})

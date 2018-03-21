from django.contrib import messages
from django.core.urlresolvers import reverse
from django.db import transaction
from django.shortcuts import redirect, render
from django.utils.translation import ugettext_lazy as _
from django.views import generic

from adhocracy4.dashboard import mixins
from adhocracy4.projects.mixins import ProjectMixin
from adhocracy4.dashboard import signals as dashboard_signals
from adhocracy4.rules import mixins as rules_mixins

from . import forms, models
from .mixins import OfflineEventFormMixin


class OfflineEventDetailView(ProjectMixin,
                             rules_mixins.PermissionRequiredMixin,
                             generic.DetailView):
    model = models.OfflineEvent
    get_context_from_object = True
    template_name = 'a4offlineevents/offlineevent_detail.html'
    permission_required = 'a4offlineevents.view_offlineevent'


class OfflineEventListView(ProjectMixin,
                           mixins.DashboardBaseMixin,
                           mixins.DashboardComponentMixin,
                           generic.ListView):
    model = models.OfflineEvent
    template_name = 'a4offlineevents/offlineevent_list.html'
    permission_required = 'a4projects.change_project'

    def get_queryset(self):
        return super().get_queryset().filter(project=self.project)

    def get_permission_object(self):
        return self.project


class OfflineEventCreateView(ProjectMixin,
                             mixins.DashboardBaseMixin,
                             mixins.DashboardComponentMixin,
                             OfflineEventFormMixin,
                             generic.TemplateView):
    template_name = 'a4offlineevents/offlineevent_create_form.html'
    permission_required = 'a4projects.change_project'

    def get_permission_object(self):
        return self.project

    def get_success_url(self):
        return reverse(
            'a4dashboard:offlineevent-list',
            kwargs={'project_slug': self.project.slug})

    def get_context_data(self, form=None, upload_forms=None, **kwargs):
        context = super().get_context_data(**kwargs)
        if not form:
            form = forms.OfflineEventForm()
        if not upload_forms:
            upload_forms = self.empty_upload_formset()
        context['form'] = form
        context['upload_forms'] = upload_forms
        return context

    def _process_formdata(self, form, upload_forms):
        form.instance.project = self.project
        with transaction.atomic():
            object = form.save()
            instances = upload_forms.save(commit=False)
            for instance in instances:
                instance.offlineevent = object
                instance.save()

    def post(self, request, *args, **kwargs):
        form = forms.OfflineEventForm(request.POST)
        upload_forms = self.filled_upload_formset(request)

        if form.is_valid() and upload_forms.is_valid():
            self._process_formdata(form, upload_forms)
            dashboard_signals.project_component_updated.send(
                sender=self.component.__class__,
                project=self.project,
                component=self.component,
                user=self.request.user
            )
            messages.success(request, _('Offline event successfully created.'))
            response = redirect(self.get_success_url())
        else:
            response = render(request,
                              self.template_name,
                              self.get_context_data(form=form,
                                                    upload_forms=upload_forms))
        return response


class OfflineEventUpdateView(ProjectMixin,
                             mixins.DashboardBaseMixin,
                             mixins.DashboardComponentMixin,
                             OfflineEventFormMixin,
                             generic.detail.SingleObjectMixin,
                             generic.TemplateView):

    model = models.OfflineEvent
    permission_required = 'a4projects.change_project'
    template_name = 'a4offlineevents/offlineevent_update_form.html'
    get_context_from_object = True

    def dispatch(self, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(*args, **kwargs)

    def get_permission_object(self):
        return self.project

    def get_success_url(self):
        return reverse(
            'a4dashboard:offlineevent-list',
            kwargs={'project_slug': self.project.slug})

    def get_context_data(self, form=None, upload_forms=None, **kwargs):
        context = super().get_context_data(**kwargs)
        if not form:
            form = forms.OfflineEventForm(instance=self.object)
        if not upload_forms:
            queryset = \
                models.OfflineEventDocument\
                .objects.filter(offlineevent=self.object)
            upload_forms = self.update_upload_formset(queryset)
        context['form'] = form
        context['upload_forms'] = upload_forms
        return context

    def _process_formdata(self, form, upload_forms):
        with transaction.atomic():
            form.save()
            instances = upload_forms.save(commit=False)
            for obj in upload_forms.deleted_objects:
                obj.delete()
            for instance in instances:
                instance.offlineevent = self.object
                instance.save()

    def post(self, request, *args, **kwargs):
        upload_forms = self.filled_upload_formset(request)
        form = forms.OfflineEventForm(request.POST, instance=self.object)
        if upload_forms.is_valid() and form.is_valid():
            self._process_formdata(form, upload_forms)
            dashboard_signals.project_component_updated.send(
                sender=self.component.__class__,
                project=self.project,
                component=self.component,
                user=self.request.user
            )
            messages.success(request, _('Offline event successfully updated.'))
            response = redirect(self.get_success_url())
        else:
            response = render(request,
                              self.template_name,
                              self.get_context_data(
                                  form=form, upload_forms=upload_forms))
        return response


class OfflineEventDeleteView(ProjectMixin,
                             mixins.DashboardBaseMixin,
                             mixins.DashboardComponentMixin,
                             mixins.DashboardComponentDeleteSignalMixin,
                             generic.DeleteView):
    model = models.OfflineEvent
    permission_required = 'a4projects.change_project'
    template_name = 'a4offlineevents/offlineevent_confirm_delete.html'
    get_context_from_object = True

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, _('Offline event has been deleted'))
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

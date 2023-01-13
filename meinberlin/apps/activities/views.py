from django.views import generic

from adhocracy4.dashboard import mixins as dashboard_mixins
from adhocracy4.projects.mixins import ProjectMixin
from adhocracy4.rules import mixins as rules_mixins

from . import forms
from . import models


class ActivityDashboardView(
    ProjectMixin,
    dashboard_mixins.DashboardBaseMixin,
    dashboard_mixins.DashboardComponentMixin,
    generic.UpdateView,
):
    model = models.Activity
    form_class = forms.ActivityForm
    template_name = "meinberlin_activities/activities_dashboard.html"
    permission_required = "meinberlin_activities.change_activity"

    def get_permission_object(self):
        return self.module

    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.instance.module = self.module
        return super().form_valid(form)

    def get_object(self, queryset=None):
        return models.Activity.objects.filter(module=self.module).first()


class ActivityView(
    ProjectMixin, rules_mixins.PermissionRequiredMixin, generic.DetailView
):
    model = models.Activity
    permission_required = "meinberlin_activities.view_activity"

    def get_object(self):
        return models.Activity.objects.filter(module=self.module).first()

    def get_permission_object(self):
        return self.module

from django.http import Http404
from django.utils.translation import ugettext_lazy as _
from django.views import generic

import adhocracy4.dashboard.mixins as dashboard_mixins
from adhocracy4.projects.mixins import ProjectMixin

from . import forms
from . import models


class FaceToFaceDashboardView(ProjectMixin,
                              dashboard_mixins.DashboardBaseMixin,
                              dashboard_mixins.DashboardComponentMixin,
                              generic.CreateView):
    model = models.Activity
    form_class = forms.ActivityForm
    template_name = 'meinberlin_facetoface/facetoface_dashboard.html'
    permission_required = 'a4projects.change_project'

    def get_permission_object(self):
        return self.project

    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.instance.module = self.module
        return super().form_valid(form)


class FaceToFaceView(ProjectMixin,
                     generic.DetailView):
    model = models.Activity

    def get_object(self):
        first_activity = models.Activity.objects \
            .filter(module=self.module) \
            .first()

        if not first_activity:
            raise Http404(_('No activity defined yet.'))
        return first_activity

from django.http import Http404
from django.utils.translation import ugettext_lazy as _
from django.views import generic

from adhocracy4.projects.mixins import ProjectMixin

from . import models


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

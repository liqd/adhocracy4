from django.views.generic.detail import DetailView

from adhocracy4.projects.models import Project

from . import models


class ProfileView(DetailView):
    model = models.User
    slug_field = 'username'

    @property
    def get_participated_projects(self):
        user = self.object

        qs = Project.objects.filter(
            action__actor=user
        ).distinct()

        return qs

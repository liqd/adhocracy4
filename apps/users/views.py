from django.db import models as django_models
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
            django_models.Q(follow__creator=user),
            django_models.Q(follow__enabled=True) |
            django_models.Q(participants=user)
        ).distinct()

        return qs

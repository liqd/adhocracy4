from django.db import models
from django.utils import timezone

from adhocracy4.projects import models as project_models


class ProjectContainer(project_models.Project):
    projects = models.ManyToManyField(
        project_models.Project,
        related_name='containers',
    )

    @property
    def not_archived_projects(self):
        return self.projects.filter(is_archived=False)

    @property
    def active_projects(self):
        now = timezone.now()
        return self.projects.filter(
            module__phase__start_date__lte=now,
            module__phase__end_date__gt=now)

    @property
    def phases(self):
        from adhocracy4.phases import models as phase_models
        return phase_models.Phase.objects\
            .filter(module__project__containers__id=self.id)

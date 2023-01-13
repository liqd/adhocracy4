from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from adhocracy4.projects import models as project_models
from adhocracy4.projects.enums import Access


class ProjectContainer(project_models.Project):
    projects = models.ManyToManyField(
        project_models.Project, related_name="containers", verbose_name=_("Projects")
    )

    @property
    def published_not_archived_projects(self):
        return self.projects.filter(is_draft=False, is_archived=False).order_by("name")

    @property
    def active_project_count(self):
        """Return the number of active projects within the container.

        A container is public by default, only public and semipublic
        projects are counted.
        """
        now = timezone.now()
        return (
            self.projects.filter(
                Q(access=Access.PUBLIC) | Q(access=Access.SEMIPUBLIC),
                is_draft=False,
                is_archived=False,
            )
            .filter(module__phase__start_date__lte=now, module__phase__end_date__gt=now)
            .distinct()
            .count()
        )

    @property
    def future_project_count(self):
        """Return the number of future projects within the container.

        A container is public by default, only public and semipublic
        projects are counted.
        """
        now = timezone.now()
        return (
            self.projects.filter(
                Q(access=Access.PUBLIC) | Q(access=Access.SEMIPUBLIC),
                is_draft=False,
                is_archived=False,
            )
            .filter(module__phase__start_date__gt=now)
            .distinct()
            .count()
        )

    @property
    def total_project_count(self):
        """Return the number of total projects within the container.

        A container is public by default, only public and semipublic
        projects are counted.
        """
        return self.projects.filter(
            Q(access=Access.PUBLIC) | Q(access=Access.SEMIPUBLIC),
            is_draft=False,
            is_archived=False,
        ).count()

    @property
    def phases(self):
        from adhocracy4.phases import models as phase_models

        return phase_models.Phase.objects.filter(
            module__project__containers__id=self.id
        )

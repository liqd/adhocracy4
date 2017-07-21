from django.db import models

from adhocracy4.projects import models as project_models


class ExternalProject(project_models.Project):
    url = models.URLField()

    @property
    def phase(self):
        return self.phases.first()

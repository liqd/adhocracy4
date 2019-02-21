from django.db import models

from adhocracy4.models import base
from adhocracy4.projects import models as project_models


class Follow(base.UserGeneratedContentModel):
    project = models.ForeignKey(project_models.Project,
                                on_delete=models.CASCADE,)
    enabled = models.BooleanField(default=True)

    class Meta:
        unique_together = ('project', 'creator')

    def __str__(self):
        return 'Follow({}, enabled={})'.format(self.project, self.enabled)

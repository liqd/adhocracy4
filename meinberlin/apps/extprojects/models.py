from django.db import models
from django.utils.translation import gettext_lazy as _

from adhocracy4.projects import models as project_models


class ExternalProject(project_models.Project):
    url = models.URLField(
        blank=True,
        verbose_name="URL",
        help_text=_("Please enter a full url which starts with https:// or http://"),
        max_length=500,
    )

    start_date = models.DateTimeField(
        blank=True, null=True, verbose_name=_("Start date")
    )
    end_date = models.DateTimeField(blank=True, null=True, verbose_name=_("End date"))

    @property
    def phase(self):
        return self.phases.first()

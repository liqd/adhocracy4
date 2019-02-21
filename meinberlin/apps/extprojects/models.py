from django.db import models
from django.utils.translation import ugettext_lazy as _

from adhocracy4.projects import models as project_models


class ExternalProject(project_models.Project):
    url = models.URLField(blank=True,
                          verbose_name='URL',
                          help_text=_('Please enter '
                                      'a full url which '
                                      'starts with https:// '
                                      'or http://'))

    @property
    def phase(self):
        return self.phases.first()

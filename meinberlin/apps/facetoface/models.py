from autoslug import AutoSlugField
from ckeditor.fields import RichTextField
from django.db import models
from django.utils.translation import ugettext_lazy as _

from adhocracy4.modules import models as module_models


class Activity(module_models.Item):
    slug = AutoSlugField(populate_from='name', unique=True)
    name = models.CharField(max_length=120, verbose_name=_('Title'))
    highlight = models.CharField(max_length=120,
                                 verbose_name=_('Highlighted Info')
                                 )
    description = RichTextField(verbose_name=_('Description'))

    def get_absolute_url(self):
        return self.project.get_absolute_url()

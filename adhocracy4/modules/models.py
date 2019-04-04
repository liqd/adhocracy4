from autoslug import AutoSlugField
from django.db import models
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from adhocracy4.models import base
from adhocracy4.projects import models as project_models


class Module(models.Model):
    slug = AutoSlugField(populate_from='name', unique=True)
    name = models.CharField(
        max_length=512,
        verbose_name=_('Title of the module'),
        help_text=_('This title will appear in the timeline and the header on '
                    'the module and project detail pages. It should be '
                    'max. 512 characters long')
    )
    description = models.CharField(
        null=True,
        blank=True,
        max_length=512,
        verbose_name=_('Short description of the module'),
        help_text=_('This short description will appear on the header of the '
                    'module and project detail pages. It should briefly state '
                    'the goal of the module in max. 512 chars.')
    )
    weight = models.PositiveIntegerField()
    project = models.ForeignKey(
        project_models.Project, on_delete=models.CASCADE)

    class Meta:
        ordering = ['weight']

    def __str__(self):
        return "{} ({})".format(self.project, self.weight)

    def get_absolute_url(self):
        return reverse('module-detail', kwargs=dict(module_slug=self.slug))

    @property
    def settings_instance(self):
        settingslist = [field.name for field in self._meta.get_fields()
                        if field.name.endswith('_settings')]
        for setting in settingslist:
            if hasattr(self, setting):
                return getattr(self, setting)

    @property
    def active_phase(self):
        return self.phase_set \
            .active_phases() \
            .first()

    @cached_property
    def phases(self):
        return self.phase_set.all()

    @cached_property
    def future_phases(self):
        return self.phase_set.future_phases()

    @cached_property
    def past_phases(self):
        return self.phase_set.past_phases()

    @property
    def last_active_phase(self):
        return self.active_phase or self.past_phases.last()

    @property
    def first_phase_start_date(self):
        first_phase = self.phase_set.order_by('start_date').first()
        return first_phase.start_date

    def has_feature(self, feature, model):
        for phase in self.phase_set.all():
            if phase.has_feature(feature, model):
                return True
        return False


class Item(base.UserGeneratedContentModel):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)

    @property
    def project(self):
        return self.module.project


class AbstractSettings(models.Model):
    module = models.OneToOneField(Module, on_delete=models.CASCADE,
                                  related_name='%(class)s_settings')

    class Meta:
        abstract = True

    @staticmethod
    def widgets():
        return {}

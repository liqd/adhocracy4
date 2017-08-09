from autoslug import AutoSlugField
from django.db import models
from django.core.urlresolvers import reverse

from adhocracy4.models import base
from adhocracy4.projects import models as project_models


class Module(models.Model):
    name = models.CharField(max_length=512, unique=True)
    slug = AutoSlugField(populate_from='name', unique=True)
    description = models.TextField(null=True, blank=True)
    weight = models.PositiveIntegerField()
    project = models.ForeignKey(
        project_models.Project, on_delete=models.CASCADE)

    class Meta:
        ordering = ['weight']

    def __str__(self):
        return "{} ({})".format(self.project, self.weight)

    def get_absolute_url(self):
        return reverse('module-detail', args=[str(self.slug)])

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

    @property
    def phases(self):
        return self.phase_set.all()

    @property
    def future_phases(self):
        return self.phase_set.future_phases()

    @property
    def past_phases(self):
        return self.phase_set.past_phases()

    @property
    def last_active_phase(self):
        return self.active_phase or self.past_phases.first()

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

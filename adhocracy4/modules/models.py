from autoslug import AutoSlugField
from django.db import models
from django.urls import reverse
from django.utils import timezone
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

    @cached_property
    def module_start(self):
        return self.phase_set.order_by('start_date').first().start_date

    @cached_property
    def module_end(self):
        return self.phase_set.order_by('-end_date').first().end_date

    @cached_property
    def module_has_started(self):
        now = timezone.now()
        return now >= self.module_start

    @cached_property
    def module_has_finished(self):
        now = timezone.now()
        return now > self.module_end

    @property
    def module_running_time_left(self):
        """
        Return the time left of the module in percent
        if it is currently running.
        """

        def seconds_in_units(seconds):
            unit_totals = []

            unit_limits = [
                           ([_('day'), _('days')], 24 * 3600),
                           ([_('hour'), _('hours')], 3600),
                           ([_('minute'), _('minutes')], 60)
                          ]

            for unit_name, limit in unit_limits:
                if seconds >= limit:
                    amount = int(float(seconds) / limit)
                    if amount > 1:
                        unit_totals.append((unit_name[1], amount))
                    else:
                        unit_totals.append((unit_name[0], amount))
                    seconds = seconds - (amount * limit)

            return unit_totals

        if self.module_has_started and not self.module_has_finished:
            now = timezone.now()
            time_delta = self.module_end - now
            seconds = time_delta.total_seconds()
            time_delta_list = seconds_in_units(seconds)
            best_unit = time_delta_list[0]
            time_delta_str = '{} {}'.format(str(best_unit[1]),
                                            str(best_unit[0]))
            return time_delta_str

        return None

    @property
    def module_running_progress(self):
        """
        Return the progress of the module in percent
        if it is currently running.
        """
        if self.module_has_started and not self.module_has_finished:
            time_gone = timezone.now() - self.module_start
            total_time = self.module_end - self.module_start
            return round(time_gone / total_time * 100)
        return None


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

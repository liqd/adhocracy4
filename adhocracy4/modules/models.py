import warnings

from autoslug import AutoSlugField
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from adhocracy4.models import base
from adhocracy4.projects import models as project_models


class ModulesQuerySet(models.QuerySet):

    def annotate_module_start(self):
        return self.annotate(module_start=models.Min('phase__start_date'))

    def annotate_module_end(self):
        return self.annotate(module_end=models.Max('phase__end_date'))

    def running_modules(self):
        """Return running modules."""
        now = timezone.now()
        return self\
            .filter(is_draft=False)\
            .annotate(module_start=models.Min('phase__start_date'))\
            .annotate(module_end=models.Max('phase__end_date'))\
            .filter(module_start__lte=now, module_end__gt=now)\
            .order_by('module_start')

    def past_modules(self):
        """Return past modules ordered by start."""
        return self\
            .filter(is_draft=False)\
            .annotate(module_start=models.Min('phase__start_date'))\
            .annotate(module_end=models.Max('phase__end_date'))\
            .filter(module_end__lte=timezone.now())\
            .order_by('module_start')

    def future_modules(self):
        """
        Return future modules ordered by start date.

        Note: Modules without a start date are assumed to start in the future.
        """
        return self\
            .filter(is_draft=False)\
            .annotate(module_start=models.Min('phase__start_date'))\
            .filter(models.Q(module_start__gt=timezone.now())
                    | models.Q(module_start=None))\
            .order_by('module_start')

    def past_and_running_modules(self):
        """Return past and running modules ordered by start date."""
        return self\
            .filter(is_draft=False)\
            .annotate(module_start=models.Min('phase__start_date'))\
            .filter(module_start__lte=timezone.now())\
            .order_by('module_start')


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
    is_draft = models.BooleanField(default=False)

    objects = ModulesQuerySet.as_manager()

    class Meta:
        ordering = ['weight']

    def __str__(self):
        return "{} ({})".format(self.project, self.weight)

    def get_absolute_url(self):
        return reverse('module-detail', kwargs=dict(module_slug=self.slug))

    @cached_property
    def get_detail_url(self):
        """
        Return either project or module detail url, depending on cluster
        and timeline logic.
        """
        if self.is_in_module_cluster:
            return self.get_absolute_url()
        elif self.project.display_timeline:
            return '{}?initialSlide={}'.format(self.project.get_absolute_url(),
                                               self.get_timeline_index)
        return self.project.get_absolute_url()

    @cached_property
    def settings_instance(self):
        settingslist = [field.name for field in self._meta.get_fields()
                        if field.name.endswith('_settings')]
        for setting in settingslist:
            if hasattr(self, setting):
                return getattr(self, setting)

    def has_feature(self, feature, model):
        for phase in self.phase_set.all():
            if phase.has_feature(feature, model):
                return True
        return False

    # Phase properties to access the modules phases
    @cached_property
    def phases(self):
        '''Return all phases for this module, ordered by weight.'''
        return self.phase_set.all()

    @cached_property
    def active_phase(self):
        '''
        Return the currently active phase of the module.

        Even though this is not enforced, there should only be one phase
        active at any given time.
        '''
        return self.phase_set \
            .active_phases() \
            .first()

    @cached_property
    def future_phases(self):
        '''Return all future phases for this module, ordered by start.'''
        return self.phase_set.future_phases()

    @cached_property
    def past_phases(self):
        '''Return all past phases for this module, ordered by start.'''
        return self.phase_set.past_phases()

    @cached_property
    def last_active_phase(self):
        '''
        Return the phase that is currently still active or the past phase
        that started last.

        The past phase that started last should also have ended last,
        because there should only be one phase running at any time.
        This is the phase that's content is shown in the module view.
        '''
        return self.active_phase or self.past_phases.last()

    # module properties combining all phases of self
    @cached_property
    def module_start(self):
        '''Return the start date of the module.'''
        return self.phase_set.order_by('start_date').first().start_date

    @cached_property
    def module_end(self):
        '''Return the end date of the module.'''
        return self.phase_set.order_by('-end_date').first().end_date

    @cached_property
    def module_has_started(self):
        '''Test if the module has already started.'''
        now = timezone.now()
        return now >= self.module_start

    @cached_property
    def module_has_finished(self):
        '''Test if the module has already finished.'''
        now = timezone.now()
        return now > self.module_end

    def seconds_in_units(self, seconds):
        '''Returns time and unit.'''
        unit_totals = []

        unit_limits = [
            ([_('day'), _('days')], 24 * 3600),
            ([_('hour'), _('hours')], 3600),
            ([_('minute'), _('minutes')], 60),
            ([_('second'), _('seconds')], 1)
        ]

        for unit_name, limit in unit_limits:
            if seconds >= limit:
                amount = int(float(seconds) / limit)
                if amount > 1:
                    unit_totals.append((unit_name[1], amount))
                else:
                    unit_totals.append((unit_name[0], amount))
                seconds = seconds - (amount * limit)
        unit_totals.append((_('seconds'), 0))

        return unit_totals

    @cached_property
    def module_starting_time_left(self):
        """
        Return the time left until the module starts.
        """

        if not self.module_has_started:
            now = timezone.now()
            time_delta = self.module_start - now
            seconds = time_delta.total_seconds()
            time_delta_list = self.seconds_in_units(seconds)
            best_unit = time_delta_list[0]
            time_delta_str = '{} {}'.format(str(best_unit[1]),
                                            str(best_unit[0]))
            return time_delta_str

        return None

    @cached_property
    def module_running_time_left(self):
        """
        Return the time left of the module if it is currently running.
        """

        if self.module_has_started and not self.module_has_finished:
            now = timezone.now()
            time_delta = self.module_end - now
            seconds = time_delta.total_seconds()
            time_delta_list = self.seconds_in_units(seconds)
            best_unit = time_delta_list[0]
            time_delta_str = '{} {}'.format(str(best_unit[1]),
                                            str(best_unit[0]))
            return time_delta_str

        return None

    @cached_property
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

    # properties to determine the timeline/cluster logic to enable multiple
    # modules in one project
    @cached_property
    def project_modules(self):
        """
        Return published modules of project.

        Used in timeline/cluster logic, so needs to be filtered for
        unpublished modules.
        """
        return self.project.module_set.filter(is_draft=False)

    @cached_property
    def other_modules(self):
        """
        Return all other published modules of project.
        """
        return self.project_modules.exclude(id=self.id)

    @cached_property
    def module_cluster(self):
        for cluster in self.project.module_clusters:
            if self in cluster:
                return cluster
        return []

    @cached_property
    def index_in_cluster(self):
        try:
            return self.module_cluster.index(self)
        except (IndexError, ValueError):
            return None

    @cached_property
    def readable_index_in_cluster(self):
        if self.index_in_cluster is not None:
            return self.index_in_cluster + 1

    @cached_property
    def is_in_module_cluster(self):
        return len(self.module_cluster) > 1

    @cached_property
    def next_module_in_cluster(self):
        if self.is_in_module_cluster:
            cluster = self.module_cluster
            idx = self.index_in_cluster
            try:
                return cluster[idx + 1]
            except IndexError:
                return None

    @cached_property
    def previous_module_in_cluster(self):
        if self.is_in_module_cluster:
            cluster = self.module_cluster
            idx = self.index_in_cluster
            try:
                if idx > 0:
                    return cluster[idx - 1]
            except IndexError:
                return None

    @cached_property
    def get_timeline_index(self):
        if self.project.display_timeline:
            for count, cluster in enumerate(self.project.participation_dates):
                if 'modules' in cluster and self in cluster['modules']:
                    return count
        return 0

    # Deprecated properties
    @cached_property
    def first_phase_start_date(self):
        '''
        Return the start date of the first phase in the module.

        Attention: This method is _deprecated_. The property module_start
        should be used instead.
        '''
        warnings.warn(
            "first_phase_start_date is deprecated; use module_start.",
            DeprecationWarning
        )
        first_phase = self.phase_set.order_by('start_date').first()
        return first_phase.start_date


class Item(base.UserGeneratedContentModel):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)

    @cached_property
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

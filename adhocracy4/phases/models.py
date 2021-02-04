import warnings
from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import F
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from adhocracy4.modules import models as modules_models

from . import content
from .validators import validate_content


class PhasesQuerySet(models.QuerySet):

    def active_phases(self):
        """Return active phases."""
        now = timezone.now()
        return self.filter(start_date__lte=now, end_date__gt=now)

    def finished_phases(self):
        """Return past phases."""
        return self.filter(end_date__lte=timezone.now())

    def past_phases(self):
        """Return past phases ordered by start date."""
        return self\
            .filter(end_date__lte=timezone.now())\
            .order_by('start_date')

    def future_phases(self):
        """
        Return future phases ordered by start date.

        Note: Phases without a start date are assumed to start in the future.
        """
        return self\
            .filter(models.Q(start_date__gt=timezone.now())
                    | models.Q(start_date=None))\
            .order_by(F('start_date').asc(nulls_first=True))

    def past_and_active_phases(self):
        """Return past and active phases ordered by start date."""
        return self\
            .filter(start_date__lte=timezone.now())\
            .order_by('start_date')

    def finish_next(self, hours=24):
        """
        All phases that are active and finish within the given time.
        """
        now = timezone.now()
        last_end_date = (now + timedelta(hours=hours))
        return self.active_phases().filter(end_date__lte=last_end_date)

    def start_last(self, hours=1):
        """
        All phases that have started within the given time.
        """
        now = timezone.now()
        first_start_date = (now - timedelta(hours=hours))
        return self.filter(start_date__gt=first_start_date, start_date__lt=now)


class Phase(models.Model):
    name = models.CharField(max_length=80, verbose_name=_('Name'))
    description = models.TextField(max_length=300,
                                   verbose_name=_('Description'))
    type = models.CharField(max_length=128, validators=[validate_content])
    module = models.ForeignKey(modules_models.Module, on_delete=models.CASCADE)
    start_date = models.DateTimeField(blank=True, null=True,
                                      verbose_name=_('Start date'))
    end_date = models.DateTimeField(blank=True, null=True,
                                    verbose_name=_('End date'))
    weight = models.IntegerField(default=0)

    objects = PhasesQuerySet.as_manager()

    class Meta:
        ordering = ['weight', 'id']

    def __str__(self):
        return '{} ({})'.format(self.name, self.type)

    def content(self):
        return content[self.type]

    def clean(self):
        if self.end_date and self.start_date:
            if self.end_date < self.start_date:
                raise ValidationError({
                    'end_date': _('End date can not be before '
                                  'start date.')
                })
        elif self.start_date and not self.end_date:
            raise ValidationError({
                'end_date': _('Either both or no date has to be set.')
            })
        elif not self.start_date and self.end_date:
            raise ValidationError({
                'start_date': _('Either both or no date has to be set.')
            })
        super().clean()

    @cached_property
    def view(self):
        return content[self.type].view

    @cached_property
    def is_over(self):
        """Test if phase is over."""
        if self.end_date:
            return self.end_date <= timezone.now()
        return True

    def has_feature(self, feature, model):
        return content[self.type].has_feature(feature, model)

    def is_first_of_project(self):
        """Test if this is the first phase of the project.

        Attention: _deprecated_ as this only works for one module where the
        phase order is determined by weight.
        """
        warnings.warn(
            "is_first_of_project is deprecated as it relies "
            "on the project only having one module",
            DeprecationWarning
        )
        return self == self.module.project.phases.first()

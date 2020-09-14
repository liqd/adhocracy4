import re
from contextlib import contextmanager
from datetime import timedelta

from django.utils import timezone
from freezegun import freeze_time


@contextmanager
def active_phase(module, phase_type):
    now = timezone.now()
    phase = module.phase_set.create(
        start_date=now,
        end_date=now + timedelta(days=1),
        name='TEST PHASE',
        description='TEST DESCRIPTION',
        type=phase_type().identifier,
        weight=0,
    )

    with freeze_time(phase.start_date):
        yield

    phase.delete()


@contextmanager
def past_phase(module, phase_type):
    now = timezone.now()
    phase = module.phase_set.create(
        start_date=now,
        end_date=now + timedelta(days=1),
        name='TEST PHASE',
        description='TEST DESCRIPTION',
        type=phase_type().identifier,
        weight=0,
    )

    with freeze_time(phase.end_date + timedelta(minutes=1)):
        yield

    phase.delete()


class pytest_regex:
    """Assert that a given string meets some expectations."""

    def __init__(self, pattern, flags=0):
        self._regex = re.compile(pattern, flags)

    def __eq__(self, actual):
        return bool(self._regex.match(str(actual)))

    def __repr__(self):
        return self._regex.pattern

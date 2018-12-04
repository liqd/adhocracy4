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

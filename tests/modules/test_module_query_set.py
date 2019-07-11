import pytest
from dateutil.parser import parse
from freezegun import freeze_time

from adhocracy4.modules import models


@pytest.mark.django_db
def test_running_modules(phase_factory):
    phase1 = phase_factory(
        start_date=parse('2013-01-01 17:00:00 UTC'),
        end_date=parse('2013-01-01 18:00:00 UTC')
    )
    module1 = phase1.module
    phase2 = phase_factory(
        start_date=parse('2013-01-01 17:00:00 UTC'),
        end_date=parse('2013-01-01 18:00:00 UTC')
    )
    module2 = phase2.module
    phase_factory(
        module=module2,
        start_date=parse('2013-01-01 18:00:00 UTC'),
        end_date=parse('2013-01-01 18:00:01 UTC')
    )
    phase4 = phase_factory(
        start_date=parse('2013-01-01 17:00:00 UTC'),
        end_date=parse('2013-01-01 19:00:00 UTC')
    )
    module3 = phase4.module
    phase_factory(
        module=module3,
        start_date=parse('2013-01-01 19:00:01 UTC'),
        end_date=parse('2013-01-01 20:00:00 UTC')
    )

    with freeze_time('2013-01-01 18:00:00 UTC'):
        all_running_modules = models.Module.objects.running_modules()
        assert module1 not in all_running_modules
        assert module2 in all_running_modules
        assert module3 in all_running_modules

        assert module2.module_start == parse('2013-01-01 17:00:00 UTC')
        assert module2.module_end == parse('2013-01-01 18:00:01 UTC')


@pytest.mark.django_db
def test_past_modules(phase_factory):
    phase1 = phase_factory(
        start_date=parse('2013-01-01 17:00:02 UTC'),
        end_date=parse('2013-01-01 18:00:00 UTC')
    )
    module1 = phase1.module
    phase2 = phase_factory(
        start_date=parse('2013-01-01 17:00:00 UTC'),
        end_date=parse('2013-01-01 18:00:00 UTC')
    )
    module2 = phase2.module
    phase_factory(
        module=module2,
        start_date=parse('2013-01-01 18:00:00 UTC'),
        end_date=parse('2013-01-01 18:00:01 UTC')
    )

    with freeze_time('2013-01-01 18:00:00 UTC'):
        past_modules = models.Module.objects.past_modules()
        assert module1 in past_modules
        assert module2 not in past_modules
        assert module1.module_start == parse('2013-01-01 17:00:02 UTC')
        assert module1.module_end == parse('2013-01-01 18:00:00 UTC')

    with freeze_time('2013-01-01 18:00:01 UTC'):
        past_modules = models.Module.objects.past_modules()
        assert module1 in past_modules
        assert module2 == past_modules.first()


@pytest.mark.django_db
def test_future_modules(phase_factory):
    phase1 = phase_factory(
        start_date=parse('2013-01-01 17:00:00 UTC'),
        end_date=parse('2013-01-01 18:00:00 UTC')
    )
    module1 = phase1.module
    phase2 = phase_factory(
        start_date=parse('2013-01-01 17:00:00 UTC'),
        end_date=parse('2013-01-01 18:00:00 UTC')
    )
    module2 = phase2.module
    phase_factory(
        module=module2,
        start_date=parse('2013-01-01 18:00:00 UTC'),
        end_date=parse('2013-01-01 18:00:01 UTC')
    )
    phase4 = phase_factory(
        start_date=parse('2013-01-01 18:00:00 UTC'),
        end_date=parse('2013-01-01 19:00:00 UTC')
    )
    module3 = phase4.module
    phase_factory(
        module=module3,
        start_date=parse('2013-01-01 19:00:01 UTC'),
        end_date=parse('2013-01-01 20:00:00 UTC')
    )

    with freeze_time('2013-01-01 16:00:00 UTC'):
        future_modules = models.Module.objects.future_modules()
        assert module1 in future_modules
        assert module2 in future_modules
        assert module3 in future_modules

    with freeze_time('2013-01-01 17:00:00 UTC'):
        future_modules = models.Module.objects.future_modules()
        assert module1 not in future_modules
        assert module2 not in future_modules
        assert module3 in future_modules


@pytest.mark.django_db
def test_past_and_running_modules(phase_factory):
    phase1 = phase_factory(
        start_date=parse('2013-01-01 17:00:00 UTC'),
        end_date=parse('2013-01-01 18:00:00 UTC')
    )
    module1 = phase1.module
    phase2 = phase_factory(
        start_date=parse('2013-01-01 17:00:00 UTC'),
        end_date=parse('2013-01-01 18:00:00 UTC')
    )
    module2 = phase2.module
    phase_factory(
        module=module2,
        start_date=parse('2013-01-01 18:00:00 UTC'),
        end_date=parse('2013-01-01 18:00:01 UTC')
    )
    phase4 = phase_factory(
        start_date=parse('2013-01-01 18:00:02 UTC'),
        end_date=parse('2013-01-01 19:00:00 UTC')
    )
    module3 = phase4.module
    phase_factory(
        module=module3,
        start_date=parse('2013-01-01 19:00:01 UTC'),
        end_date=parse('2013-01-01 20:00:00 UTC')
    )

    with freeze_time('2013-01-01 18:00:00 UTC'):
        past_and_running_modules = \
            models.Module.objects.past_and_running_modules()
        assert module1 in past_and_running_modules
        assert module2 in past_and_running_modules
        assert module3 not in past_and_running_modules

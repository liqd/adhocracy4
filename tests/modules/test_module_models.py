from datetime import timedelta
import pytest

from tests.apps.questions import models as q_models


@pytest.mark.django_db
def test_has_feature(phase):
    module = phase.module
    assert module.has_feature('crud', q_models.Question)


@pytest.mark.django_db
def test_first_phase_start_date(phase, phase_factory):
    module = phase.module
    first_phase = phase_factory(
        module=module, start_date=phase.start_date - timedelta(days=1))
    assert module.first_phase_start_date == first_phase.start_date

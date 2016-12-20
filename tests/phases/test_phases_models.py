import pytest
from dateutil.parser import parse
from django.core.exceptions import ValidationError
from freezegun import freeze_time

from adhocracy4.phases import models, content
from tests.apps.questions import models as q_models
from tests.apps.questions import views as q_views



@pytest.mark.django_db
def test_manager_active_phases(phase_factory):

    old_phase1 = phase_factory(
        start_date=parse('2013-01-01 17:00:00 UTC'),
        end_date=parse('2013-01-01 18:00:00 UTC')
    )
    module = old_phase1.module
    active_phase1 = phase_factory(
        module=module,
        start_date=parse('2013-01-01 18:00:00 UTC'),
        end_date=parse('2013-01-01 18:00:01 UTC')
    )
    active_phase2 = phase_factory(
        start_date=parse('2013-01-01 17:00:00 UTC'),
        end_date=parse('2013-01-01 19:00:00 UTC')
    )
    future_phase1 = phase_factory(
        start_date=parse('2013-01-01 18:00:01 UTC'),
        end_date=parse('2013-01-01 18:00:00 UTC')
    )

    with freeze_time('2013-01-01 18:00:00 UTC'):
        all_active_phases = models.Phase.objects.active_phases()
        assert active_phase1 in all_active_phases
        assert active_phase2 in all_active_phases
        assert old_phase1 not in all_active_phases
        assert future_phase1 not in all_active_phases

        module_active_phases = module.phase_set.active_phases()
        assert len(module_active_phases) == 1
        assert active_phase1 in module_active_phases


@pytest.mark.django_db
def test_manager_finished_phases(phase_factory):
    old_phase = phase_factory(
        start_date=parse('2013-01-01 17:00:00 UTC'),
        end_date=parse('2013-01-01 18:00:00 UTC')
    )

    new_phase = phase_factory(
        start_date=parse('2013-01-01 18:00:00 UTC'),
        end_date=parse('2013-01-01 19:00:00 UTC')
    )

    with freeze_time(new_phase.start_date):
        finished_phases = models.Phase.objects.finished_phases()
        assert list(finished_phases) == [old_phase]

    with freeze_time(new_phase.end_date):
        finished_phases = models.Phase.objects.finished_phases()
        assert list(finished_phases) == [old_phase, new_phase]


@pytest.mark.django_db
def test_manager_finish_next(phase_factory):

    phase_today = phase_factory(
        start_date=parse('2013-01-01 17:00:00 UTC'),
        end_date=parse('2013-01-01 17:00:01 UTC')
    )

    phase_tomorrow = phase_factory(
        start_date=parse('2013-01-01 17:00:00 UTC'),
        end_date=parse('2013-01-02 17:00:00 UTC')
    )

    phase_after_tomorrow = phase_factory(
        start_date=parse('2013-01-01 17:00:00 UTC'),
        end_date=parse('2013-01-02 17:00:03 UTC')
    )

    with freeze_time(phase_today.start_date):
        finish_phases = models.Phase.objects.finish_next()
        assert list(finish_phases) == [phase_today, phase_tomorrow]

    with freeze_time(phase_today.end_date):
        finish_phases = models.Phase.objects.finish_next()
        assert list(finish_phases) == [phase_tomorrow]


@pytest.mark.django_db
def test_phase_validation(phase_factory):
    invalid_phase = phase_factory(
        start_date=parse('2013-01-01 18:00:01 UTC'),
        end_date=parse('2013-01-01 16:00:00 UTC')
    )

    with freeze_time('2013-01-01 18:00:00 UTC'):
        all_active_phases = models.Phase.objects.active_phases()
        assert invalid_phase not in all_active_phases

        with pytest.raises(ValidationError):
            models.Phase.clean(invalid_phase)

    valid_phase = phase_factory(
        start_date=parse('2013-01-01 16:00:00 UTC'),
        end_date=parse('2013-01-01 16:00:01 UTC')
    )

    valid_phase.clean()


@pytest.mark.django_db
def test_questionsapp_phase_view(phase):
    assert phase.view == q_views.QuestionList


@pytest.mark.django_db
def test_questionsapp_phase_feature(phase):
    assert phase.has_feature('crud', q_models.Question)


@pytest.mark.django_db
def test_questionsapp_phase_content(phase):
    assert phase.content() is content['a4test_questions:020:ask']


@pytest.mark.django_db
def test_is_over_property(phase):
    with freeze_time(phase.start_date):
        assert phase.is_over is False
    with freeze_time(phase.end_date):
        assert phase.is_over is True

@pytest.mark.django_db
def test_str(phase):
    str(phase) == "AskPhase (a4test_questions:020:ask)"

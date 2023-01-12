from datetime import timedelta

import pytest
from dateutil.parser import parse
from django.core.exceptions import ValidationError
from freezegun import freeze_time

from adhocracy4.phases import content
from adhocracy4.phases import models
from tests.apps.questions import models as q_models
from tests.apps.questions import views as q_views


@pytest.mark.django_db
def test_manager_active_phases(phase_factory):

    old_phase1 = phase_factory(
        start_date=parse("2013-01-01 17:00:00 UTC"),
        end_date=parse("2013-01-01 18:00:00 UTC"),
    )
    module = old_phase1.module
    active_phase1 = phase_factory(
        module=module,
        start_date=parse("2013-01-01 18:00:00 UTC"),
        end_date=parse("2013-01-01 18:00:01 UTC"),
    )
    active_phase2 = phase_factory(
        start_date=parse("2013-01-01 17:00:00 UTC"),
        end_date=parse("2013-01-01 19:00:00 UTC"),
    )
    future_phase1 = phase_factory(
        start_date=parse("2013-01-01 18:00:01 UTC"),
        end_date=parse("2013-01-01 18:00:00 UTC"),
    )

    with freeze_time("2013-01-01 18:00:00 UTC"):
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
        start_date=parse("2013-01-01 17:00:00 UTC"),
        end_date=parse("2013-01-01 18:00:00 UTC"),
    )

    new_phase = phase_factory(
        start_date=parse("2013-01-01 18:00:00 UTC"),
        end_date=parse("2013-01-01 19:00:00 UTC"),
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
        start_date=parse("2013-01-01 17:00:00 UTC"),
        end_date=parse("2013-01-01 17:00:01 UTC"),
    )

    phase_tomorrow = phase_factory(
        start_date=parse("2013-01-01 17:00:00 UTC"),
        end_date=parse("2013-01-02 17:00:00 UTC"),
    )

    phase_factory(
        start_date=parse("2013-01-01 17:00:00 UTC"),
        end_date=parse("2013-01-02 17:00:03 UTC"),
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
        start_date=parse("2013-01-01 18:00:01 UTC"),
        end_date=parse("2013-01-01 16:00:00 UTC"),
    )

    with freeze_time("2013-01-01 18:00:00 UTC"):
        all_active_phases = models.Phase.objects.active_phases()
        assert invalid_phase not in all_active_phases

        with pytest.raises(ValidationError):
            models.Phase.clean(invalid_phase)

    valid_phase = phase_factory(
        start_date=parse("2013-01-01 16:00:00 UTC"),
        end_date=parse("2013-01-01 16:00:01 UTC"),
    )

    valid_phase.clean()

    invalid_phase2 = phase_factory(
        start_date=None, end_date=parse("2013-01-01 16:00:00 UTC")
    )
    invalid_phase3 = phase_factory(
        start_date=parse("2013-01-01 18:00:01 UTC"), end_date=None
    )
    with pytest.raises(ValidationError):
        models.Phase.clean(invalid_phase2)
    with pytest.raises(ValidationError):
        models.Phase.clean(invalid_phase3)


@pytest.mark.django_db
def test_questionsapp_phase_view(phase_factory):
    phase = phase_factory(type="a4test_questions:ask")
    assert phase.view == q_views.QuestionList


@pytest.mark.django_db
def test_questionsapp_phase_feature(phase_factory):
    phase = phase_factory(type="a4test_questions:ask")
    assert phase.has_feature("crud", q_models.Question)


@pytest.mark.django_db
def test_questionsapp_phase_content(phase_factory):
    phase = phase_factory(type="a4test_questions:ask")
    assert phase.content() is content["a4test_questions:ask"]


@pytest.mark.django_db
def test_is_over_property(phase_factory):
    phase1 = phase_factory()
    phase2 = phase_factory()
    phase3 = phase_factory(start_date=None, end_date=None)
    with freeze_time(phase1.start_date):
        assert phase1.is_over is False
    with freeze_time(phase2.end_date):
        assert phase2.is_over is True
    assert phase3.is_over is True


@pytest.mark.django_db
def test_str(phase):
    str(phase) == "AskPhase (a4test_questions:ask)"


@pytest.mark.django_db
def test_past_phases(phase_factory):
    phase1 = phase_factory(
        start_date=parse("2013-01-01 18:00:00 UTC"),
        end_date=parse("2013-01-10 18:00:00 UTC"),
    )
    phase2 = phase_factory(
        start_date=parse("2013-01-05 18:00:00 UTC"),
        end_date=parse("2013-01-15 18:00:00 UTC"),
    )

    with freeze_time(phase1.start_date):
        assert list(models.Phase.objects.past_phases()) == []
    with freeze_time(phase1.end_date):
        assert list(models.Phase.objects.past_phases()) == [phase1]
    with freeze_time(phase2.end_date):
        assert list(models.Phase.objects.past_phases()) == [phase1, phase2]


@pytest.mark.django_db
def test_future_phases(phase_factory):
    phase1 = phase_factory(
        start_date=parse("2013-01-01 18:00:00 UTC"),
        end_date=parse("2013-01-10 18:00:00 UTC"),
    )
    phase2 = phase_factory(
        start_date=parse("2013-01-05 18:00:00 UTC"),
        end_date=parse("2013-01-15 18:00:00 UTC"),
    )
    phase3 = phase_factory(start_date=None, end_date=None)

    with freeze_time(phase1.start_date - timedelta(minutes=1)):
        assert list(models.Phase.objects.future_phases()) == [phase1, phase2, phase3]
    with freeze_time(phase2.start_date - timedelta(minutes=1)):
        assert list(models.Phase.objects.future_phases()) == [phase2, phase3]
    with freeze_time(phase2.end_date):
        assert list(models.Phase.objects.future_phases()) == [phase3]


@pytest.mark.django_db
def test_past_and_active_phases(phase_factory):

    phase1 = phase_factory(
        start_date=parse("2013-01-01 18:00:00 UTC"),
        end_date=parse("2013-01-10 18:00:00 UTC"),
    )
    phase2 = phase_factory(
        start_date=parse("2013-01-05 18:00:00 UTC"),
        end_date=parse("2013-01-15 18:00:00 UTC"),
    )
    phase_factory(start_date=None, end_date=None)

    with freeze_time(phase1.start_date - timedelta(minutes=1)):
        assert list(models.Phase.objects.past_and_active_phases()) == []
    with freeze_time(phase1.start_date):
        assert list(models.Phase.objects.past_and_active_phases()) == [phase1]
    with freeze_time(phase2.start_date):
        assert list(models.Phase.objects.past_and_active_phases()) == [phase1, phase2]
    with freeze_time(phase2.end_date):
        assert list(models.Phase.objects.past_and_active_phases()) == [phase1, phase2]


@pytest.mark.django_db
def test_starts_first_of_project(phase_factory, module_factory, project_factory):
    project1 = project_factory()
    module1 = module_factory(weight=1, project=project1)
    module2 = module_factory(weight=2, project=project1)
    # phase1 is after phase2, but is in a module with lower weight
    phase1 = phase_factory(
        module=module1,
        start_date=parse("2022-01-20 17:00:00 UTC"),
        end_date=parse("2022-01-24 18:00:00 UTC"),
    )
    phase2 = phase_factory(
        module=module2,
        start_date=parse("2022-01-15 17:00:00 UTC"),
        end_date=parse("2022-01-19 18:00:00 UTC"),
    )

    assert phase1.starts_first_of_project() is False
    assert phase2.starts_first_of_project() is True

    phase3 = phase_factory(
        start_date=parse("2022-01-20 17:00:00 UTC"),
        end_date=parse("2022-01-24 18:00:00 UTC"),
    )
    phase4 = phase_factory(
        module=phase3.module,
        start_date=None,
        end_date=None,
    )
    assert phase3.starts_first_of_project() is True
    assert phase4.starts_first_of_project() is False

    phase5 = phase_factory(
        start_date=None,
        end_date=None,
    )
    assert phase5.starts_first_of_project() is True

    # phase in a not published module should not be taken
    # into consideration
    module3 = module_factory(is_draft=True)
    phase6 = phase_factory(
        module=module3,
        start_date=parse("2022-01-20 17:00:00 UTC"),
        end_date=parse("2022-01-24 18:00:00 UTC"),
    )
    assert phase6.starts_first_of_project() is False

    project2 = project_factory()
    module4 = module_factory(is_draft=True, project=project2)
    module5 = module_factory(is_draft=False, project=project2)
    # phase7 is before phase8, but is in an unpublished module
    phase7 = phase_factory(
        module=module4,
        start_date=parse("2022-01-15 17:00:00 UTC"),
        end_date=parse("2022-01-19 18:00:00 UTC"),
    )
    phase8 = phase_factory(
        module=module5,
        start_date=parse("2022-01-20 17:00:00 UTC"),
        end_date=parse("2022-01-24 18:00:00 UTC"),
    )
    assert phase7.starts_first_of_project() is False
    assert phase8.starts_first_of_project() is True

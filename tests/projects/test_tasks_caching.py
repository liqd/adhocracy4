from datetime import datetime
from datetime import timedelta
from datetime import timezone

import pytest
from django.core.cache import cache
from freezegun import freeze_time

from meinberlin.apps.projects.tasks import get_next_projects_end
from meinberlin.apps.projects.tasks import get_next_projects_start
from meinberlin.apps.projects.tasks import schedule_reset_cache_for_projects


@pytest.mark.django_db
def test_task_schedule_reset_cache_for_projects_becoming_active(
    client, phase_factory, project_factory, django_assert_num_queries
):
    n_objects = 6
    objects = project_factory.create_batch(size=n_objects)

    # make dates to work with phase_factory
    now = datetime.now(tz=timezone.utc)
    last_week = now - timedelta(days=7)
    next_week = now + timedelta(days=7)

    # make active projects
    active_projects = objects[:3]
    for proj in active_projects:
        phase_factory(
            start_date=last_week,
            end_date=next_week,
            module__project=proj,
        )
    # make future projects
    count = 2
    future_projects = objects[3:6]
    for proj in future_projects:
        phase_factory(
            start_date=now + timedelta(minutes=count),
            end_date=next_week,
            module__project=proj,
        )
        count += 2

    # check function get_next_projects_start
    with django_assert_num_queries(1):
        future_projects_timestamps = get_next_projects_start()
    assert len(future_projects) == len(future_projects_timestamps)

    # call celery task inline as a function
    with freeze_time(now):
        next_projects_start = cache.get("next_projects_start")
        assert next_projects_start is not None
        assert next_projects_start == future_projects_timestamps

        result = schedule_reset_cache_for_projects()
        assert result is True

    with freeze_time(now + timedelta(minutes=11)):
        result = schedule_reset_cache_for_projects()
        assert result is False

        next_projects_start = cache.get("next_projects_start")
        assert next_projects_start is None


@pytest.mark.django_db
def test_task_schedule_reset_cache_for_projects_becoming_past(
    client, phase_factory, project_factory, django_assert_num_queries
):
    n_objects = 4
    objects = project_factory.create_batch(size=n_objects)

    # make dates to work with phase_factory
    now = datetime.now(tz=timezone.utc)
    last_week = now - timedelta(days=7)
    next_week = now + timedelta(days=7)

    # make active projects
    active_projects = objects[:3]
    for proj in active_projects:
        phase_factory(
            start_date=last_week,
            end_date=next_week,
            module__project=proj,
        )

    # make project that will become past in the next 10 mins
    become_past_project = objects[3]
    phase_factory(
        start_date=last_week,
        end_date=now + timedelta(minutes=5),
        module__project=become_past_project,
    )
    # check function get_next_projects_start
    with django_assert_num_queries(1):
        project_timestamps = get_next_projects_end()

    str_end_date = become_past_project.end_date.strftime("%Y-%m-%d, %H:%M:%S %Z")
    assert str_end_date == project_timestamps[0][0]

    # call celery task inline as a function
    with freeze_time(now):
        next_projects_end = cache.get("next_projects_end")
        assert next_projects_end is not None
        assert next_projects_end == project_timestamps

        result = schedule_reset_cache_for_projects()
        assert result is True

    with freeze_time(now + timedelta(minutes=11)):
        result = schedule_reset_cache_for_projects()
        assert result is False

        next_projects_end = cache.get("next_projects_end")
        assert next_projects_end is None

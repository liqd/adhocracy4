from datetime import datetime
from datetime import timedelta
from datetime import timezone

import pytest
from django.core.cache import cache
from django.db.models import signals
from django.urls import reverse
from factory.django import mute_signals
from freezegun import freeze_time

from adhocracy4.projects.enums import Access
from adhocracy4.test.helpers import redirect_target
from meinberlin.apps.projects.tasks import get_next_projects_end
from meinberlin.apps.projects.tasks import get_next_projects_start
from meinberlin.apps.projects.tasks import schedule_reset_cache_for_projects
from meinberlin.apps.projects.tasks import set_cache_for_projects
from meinberlin.apps.projects.tasks import set_ext_projects_cache
from meinberlin.apps.projects.tasks import set_plans_cache
from meinberlin.apps.projects.tasks import set_public_projects_cache
from meinberlin.test.factories.extprojects import ExternalProjectFactory
from meinberlin.test.factories.plans import PlanFactory


@pytest.mark.django_db
def test_task_schedule_reset_cache_for_projects_becoming_active(
    phase_factory, project_factory, django_assert_num_queries
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

    cache.clear()
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

    cache.clear()
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

    cache.clear()
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

    cache.clear()
    with freeze_time(now + timedelta(minutes=11)):
        result = schedule_reset_cache_for_projects()
        assert result is False

        next_projects_end = cache.get("next_projects_end")
        assert next_projects_end is None


@pytest.mark.django_db
def test_task_queries_for_plans(django_assert_num_queries):
    n_objects = 6
    PlanFactory.create_batch(size=n_objects)
    with django_assert_num_queries(3):
        set_plans_cache()


@pytest.mark.django_db
def test_task_queries_for_extprojects(django_assert_num_queries):
    n_objects = 6
    ExternalProjectFactory.create_batch(
        size=n_objects, access=Access.PUBLIC, is_draft=False, is_archived=False
    )
    now = datetime.now(tz=timezone.utc)
    with django_assert_num_queries(62):
        set_ext_projects_cache(now)


@pytest.mark.django_db
def test_task_queries_for_projects(
    project_factory, phase_factory, django_assert_num_queries
):
    n_objects = 6
    objects = project_factory.create_batch(size=n_objects)

    # make dates to work with phase_factory
    now = datetime.now(tz=timezone.utc)
    last_week = now - timedelta(days=7)
    next_week = now + timedelta(days=7)

    # make active projects
    active_projects = objects[:2]
    for proj in active_projects:
        phase_factory(
            start_date=last_week,
            end_date=next_week,
            module__project=proj,
        )

    # make past project
    past_project = objects[2]
    phase_factory(
        start_date=last_week,
        end_date=now - timedelta(minutes=5),
        module__project=past_project,
    )

    # make future project
    future_project = objects[3]
    phase_factory(
        start_date=next_week,
        end_date=next_week + timedelta(days=7),
        module__project=future_project,
    )

    now = datetime.now(tz=timezone.utc)
    with django_assert_num_queries(73):
        set_public_projects_cache(now)


@pytest.mark.django_db
def test_plan_signals_only_change_plan_cache(
    django_capture_on_commit_callbacks, project_factory
):
    n_objects = 6
    with mute_signals(signals.post_save, signals.post_delete):
        projects = project_factory.create_batch(size=n_objects)
        plans = PlanFactory.create_batch(size=n_objects)
        ext_projects = ExternalProjectFactory.create_batch(
            size=n_objects, access=Access.PUBLIC, is_draft=False, is_archived=False
        )
        set_cache_for_projects()
        projects[0].delete()
        ext_projects[0].delete()
    with django_capture_on_commit_callbacks(execute=True):
        plans[0].delete()
    assert len(cache.get("projects_")) == n_objects
    assert len(cache.get("extprojects")) == n_objects
    assert len(cache.get("plans")) == n_objects - 1


@pytest.mark.django_db
def test_ext_project_signals_only_change_ext_projects_and_projects_cache(
    django_capture_on_commit_callbacks, project_factory
):
    n_objects = 6
    with mute_signals(signals.post_save, signals.post_delete):
        projects = project_factory.create_batch(size=n_objects)
        plans = PlanFactory.create_batch(size=n_objects)
        ext_projects = ExternalProjectFactory.create_batch(
            size=n_objects, access=Access.PUBLIC, is_draft=False, is_archived=False
        )
        set_cache_for_projects()
        projects[0].delete()
        plans[0].delete()
    with django_capture_on_commit_callbacks(execute=True):
        ext_projects[0].delete()
    assert len(cache.get("plans")) == n_objects
    # as ExternalProject is a child class of Project, the post_delete signal for Project is also called
    assert len(cache.get("projects_")) == n_objects - 1
    assert len(cache.get("extprojects")) == n_objects - 1


@pytest.mark.django_db
def test_project_signals_only_change_projects_cache(
    django_capture_on_commit_callbacks, project_factory
):
    n_objects = 6
    with mute_signals(signals.post_save, signals.post_delete):
        projects = project_factory.create_batch(size=n_objects)
        plans = PlanFactory.create_batch(size=n_objects)
        ext_projects = ExternalProjectFactory.create_batch(
            size=n_objects, access=Access.PUBLIC, is_draft=False, is_archived=False
        )
        set_cache_for_projects()
        ext_projects[0].delete()
        plans[0].delete()
    with django_capture_on_commit_callbacks(execute=True):
        projects[0].delete()
    assert len(cache.get("plans")) == n_objects
    assert len(cache.get("extprojects")) == n_objects
    assert len(cache.get("projects_")) == n_objects - 1


@pytest.mark.django_db
@pytest.mark.parametrize(
    "namespace,factory,factory_kwargs",
    [
        ("plans", PlanFactory, {}),
        (
            "extprojects",
            ExternalProjectFactory,
            {"access": Access.PUBLIC, "is_draft": False, "is_archived": False},
        ),
    ],
)
def test_task_reset_for_plans_and_exprojects(
    namespace, factory, factory_kwargs, django_assert_num_queries
):
    n_objects = 6
    cache_key = namespace

    factory.create_batch(size=n_objects, **factory_kwargs)

    now = datetime.now(tz=timezone.utc)

    # check function set_cache_for_projects
    set_cache_for_projects()

    from freezegun import freeze_time

    with freeze_time(now):
        with django_assert_num_queries(0):
            # 0 number of queries means the api results are cached
            cache_projects = cache.get(cache_key)
            assert len(cache_projects) == 6


@pytest.mark.django_db
def test_task_reset_cache_for_projects(
    phase_factory, project_factory, django_assert_num_queries
):
    n_objects = 6
    objects = project_factory.create_batch(size=n_objects)

    # make dates to work with phase_factory
    now = datetime.now(tz=timezone.utc)
    last_week = now - timedelta(days=7)
    next_week = now + timedelta(days=7)

    # make active projects
    active_projects = objects[:2]
    for proj in active_projects:
        phase_factory(
            start_date=last_week,
            end_date=next_week,
            module__project=proj,
        )

    # make past project
    past_project = objects[2]
    phase_factory(
        start_date=last_week,
        end_date=now - timedelta(minutes=5),
        module__project=past_project,
    )

    # make future project
    future_project = objects[3]
    phase_factory(
        start_date=next_week,
        end_date=next_week + timedelta(days=7),
        module__project=future_project,
    )

    # check function set_cache_for_projects
    set_cache_for_projects()

    with freeze_time(now):
        with django_assert_num_queries(0):
            active_projects = cache.get("projects_activeParticipation")
            future_project = cache.get("projects_futureParticipation")
            past_project = cache.get("projects_pastParticipation")
            projects = cache.get("projects_")
            assert len(active_projects) == 2
            assert len(past_project) == 1
            assert len(future_project) == 1
            # 2 active, 1 past, 1 future, 2 unspecified
            assert len(projects) == 6


@pytest.mark.django_db
def test_new_phase_resets_cache(
    phase_factory,
    project_factory,
    django_assert_num_queries,
    django_capture_on_commit_callbacks,
):
    n_objects = 3
    objects = project_factory.create_batch(size=n_objects)

    # make dates to work with phase_factory
    now = datetime.now(tz=timezone.utc)
    last_week = now - timedelta(days=7)
    next_week = now + timedelta(days=7)

    # make active projects
    active_project = objects[0]
    phase_factory(
        start_date=last_week,
        end_date=next_week,
        module__project=active_project,
    )

    past_project = objects[1]
    phase_factory(
        start_date=last_week,
        end_date=last_week + timedelta(days=6),
        module__project=past_project,
    )
    # make future project
    future_project = objects[2]
    phase_factory(
        start_date=next_week,
        end_date=next_week + timedelta(days=7),
        module__project=future_project,
    )

    # check function set_cache_for_projects
    set_cache_for_projects()

    with freeze_time(now):
        with django_assert_num_queries(0):
            active_projects = cache.get("projects_activeParticipation")
            past_projects = cache.get("projects_pastParticipation")
            future_projects = cache.get("projects_futureParticipation")
            assert len(active_projects) == 1
            assert len(past_projects) == 1
            assert len(future_projects) == 1

    # turn past and future project into active project
    with django_capture_on_commit_callbacks(execute=True):
        phase_factory(
            start_date=last_week,
            end_date=next_week,
            module__project=future_project,
        )
        phase_factory(
            start_date=last_week,
            end_date=next_week,
            module__project=past_project,
        )

    with freeze_time(now):
        with django_assert_num_queries(0):
            active_projects = cache.get("projects_activeParticipation")
            past_projects = cache.get("projects_pastParticipation")
            future_projects = cache.get("projects_futureParticipation")
            assert len(active_projects) == 3
            assert len(past_projects) == 0
            assert len(future_projects) == 0


@pytest.mark.django_db
def test_module_publish_resets_cache(
    client,
    user,
    phase_factory,
    project_factory,
    django_assert_num_queries,
    django_capture_on_commit_callbacks,
):
    n_objects = 3
    objects = project_factory.create_batch(size=n_objects)

    # make dates to work with phase_factory
    now = datetime.now(tz=timezone.utc)
    last_week = now - timedelta(days=7)
    next_week = now + timedelta(days=7)

    # make active projects
    active_project = objects[0]
    phase_factory(
        start_date=last_week,
        end_date=next_week,
        module__project=active_project,
    )

    past_project = objects[1]
    phase_factory(
        start_date=last_week,
        end_date=last_week + timedelta(days=6),
        module__project=past_project,
    )
    # make future project
    future_project = objects[2]
    phase_factory(
        start_date=next_week,
        end_date=next_week + timedelta(days=7),
        module__project=future_project,
    )

    # check function set_cache_for_projects
    set_cache_for_projects()

    # check projects got cached correctly
    with freeze_time(now):
        with django_assert_num_queries(0):
            active_projects = cache.get("projects_activeParticipation")
            past_projects = cache.get("projects_pastParticipation")
            future_projects = cache.get("projects_futureParticipation")
            assert len(active_projects) == 1
            assert len(past_projects) == 1
            assert len(future_projects) == 1

    # turn future project into active
    phase_active = phase_factory(
        start_date=last_week,
        end_date=next_week,
        module__project=future_project,
    )
    # turn past project into future project
    phase_future = phase_factory(
        start_date=next_week,
        end_date=next_week + timedelta(days=7),
        module__project=past_project,
    )

    module1 = phase_active.module
    module2 = phase_future.module
    module1.is_draft = True
    module2.is_draft = True

    with django_capture_on_commit_callbacks(execute=True):
        module1.save()
        module2.save()

    # check cache didn't change (as new modules are not published)
    with freeze_time(now):
        with django_assert_num_queries(0):
            active_projects = cache.get("projects_activeParticipation")
            past_projects = cache.get("projects_pastParticipation")
            future_projects = cache.get("projects_futureParticipation")
            assert len(active_projects) == 1
            assert len(past_projects) == 1
            assert len(future_projects) == 1

    module1_publish_url = reverse(
        "a4dashboard:module-publish", kwargs={"module_slug": module1.slug}
    )
    module2_publish_url = reverse(
        "a4dashboard:module-publish", kwargs={"module_slug": module2.slug}
    )

    data = {"action": "publish"}
    organisation = module1.project.organisation
    organisation.initiators.add(user)
    organisation = module2.project.organisation
    organisation.initiators.add(user)

    # publish new modules
    with django_capture_on_commit_callbacks(execute=True):
        client.login(username=user, password="password")
        response = client.post(module1_publish_url, data)
        assert redirect_target(response) == "project-edit"
        client.login(username=user, password="password")
        response = client.post(module2_publish_url, data)
        assert redirect_target(response) == "project-edit"

    module1.refresh_from_db()
    assert module1.is_draft is False
    module2.refresh_from_db()
    assert module2.is_draft is False

    # check cache was updated correctly
    with freeze_time(now):
        with django_assert_num_queries(0):
            active_projects = cache.get("projects_activeParticipation")
            past_projects = cache.get("projects_pastParticipation")
            future_projects = cache.get("projects_futureParticipation")
            assert len(active_projects) == 2
            assert len(past_projects) == 0
            assert len(future_projects) == 1

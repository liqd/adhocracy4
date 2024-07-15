from datetime import datetime
from datetime import timedelta
from datetime import timezone

import pytest
from dateutil.parser import parse
from django.core.cache import cache
from django.urls import reverse

from adhocracy4.projects.enums import Access
from adhocracy4.test.factories import PhaseFactory
from adhocracy4.test.factories import ProjectFactory
from meinberlin.apps.projects.tasks import set_cache_for_projects
from meinberlin.test.factories.extprojects import ExternalProjectFactory
from meinberlin.test.factories.plans import PlanFactory


@pytest.mark.django_db
@pytest.mark.parametrize(
    "namespace,url_name,factory,factory_kwargs",
    [
        ("plans", "plans-list", PlanFactory, {}),
        (
            "extprojects",
            "extprojects-list",
            ExternalProjectFactory,
            {"access": Access.PUBLIC, "is_draft": False, "is_archived": False},
        ),
    ],
)
def test_calling_plans_extprojects_list_creates_cached_value(
    client, namespace, url_name, factory, factory_kwargs, django_assert_num_queries
):
    n_objects = 3
    cache_key = namespace
    cache_value_before = cache.get(cache_key)

    objects = factory.create_batch(size=n_objects, **factory_kwargs)

    # check cache is set when calling the endpoint
    url = reverse(url_name)
    response = client.get(url)
    cache_value_after = cache.get(cache_key)

    assert response.status_code == 200
    assert cache_value_before is None
    assert len(cache_value_after) == len(objects) == n_objects
    assert response.status_code == 200
    assert response.data == cache_value_after

    # check if query cache refrains from hitting the db
    with django_assert_num_queries(0):
        response = client.get(url)
        assert response.status_code == 200
        assert len(response.data) == len(objects) == n_objects

    # check cache is clear when updating an object
    obj = objects[0]  # fetch the first object
    obj.config_name = "admin"
    obj.save()
    cache_value_post_saving = cache.get(cache_key)
    cache_value_post_saving is None

    # check cache is clear when deleting an object
    obj = objects[0]  # fetch the first object
    obj.delete()
    cache_value_post_saving = cache.get(cache_key)
    cache_value_post_saving is None

    # check cache is set when calling the endpoint
    response = client.get(url)
    cache_value_after = cache.get(cache_key)
    assert len(cache_value_after) == len(objects) - 1 == n_objects - 1

    # check cache is clear when creating a new object
    factory.create(**factory_kwargs)
    cache_value_post_saving = cache.get(cache_key)
    cache_value_post_saving is None

    # check cache is set when calling the endpoint
    response = client.get(url)
    cache_value_after = cache.get(cache_key)
    assert len(cache_value_after) == len(objects) == n_objects

    cache.delete(cache_key)


@pytest.mark.django_db
@pytest.mark.parametrize(
    "namespace,statustype,url_name,phase_factory,factory",
    [
        (
            "projects_",
            "activeParticipation",
            "projects-list",
            PhaseFactory,
            ProjectFactory,
        ),
        (
            "projects_",
            "futureParticipation",
            "projects-list",
            PhaseFactory,
            ProjectFactory,
        ),
        (
            "projects_",
            "pastParticipation",
            "projects-list",
            PhaseFactory,
            ProjectFactory,
        ),
    ],
)
def test_calling_list_api_creates_cached_value(
    client,
    namespace,
    statustype,
    url_name,
    phase_factory,
    factory,
    django_assert_num_queries,
):
    n_objects = 3
    cache_key = namespace + statustype
    cache_value_before = cache.get(cache_key)

    objects = factory.create_batch(size=n_objects)

    # make dates to work with phase_factory
    now = parse("2023-10-11 18:00:00 UTC")
    yesterday = now - timedelta(days=1)
    tomorrow = now + timedelta(days=1)
    last_week = now - timedelta(days=7)
    next_week = now + timedelta(days=7)

    # assign phases to projects
    if "active" in statustype:
        # make them active projects
        for project_active in objects:
            phase_factory(
                start_date=last_week,
                end_date=next_week,
                module__project=project_active,
            )
    if "future" in statustype:
        # make them future projects
        for project_future in objects:
            phase_factory(
                start_date=tomorrow,
                end_date=next_week,
                module__project=project_future,
            )
    if "past" in statustype:
        # make them past projects
        for project_past in objects:
            phase_factory(
                start_date=last_week,
                end_date=yesterday,
                module__project=project_past,
            )

    from freezegun import freeze_time

    with freeze_time(now):
        url = reverse(url_name) + f"?status={statustype}"
        response = client.get(url)
        cache_value_after = cache.get(cache_key)

        assert response.status_code == 200
        assert cache_value_before is None
        assert len(cache_value_after) == len(objects) == n_objects
        assert response.status_code == 200
        assert response.data == cache_value_after

        with django_assert_num_queries(0):
            url = reverse(url_name) + f"?status={statustype}"
            response = client.get(url)
            assert response.status_code == 200
            assert response.data == cache_value_after

        cache.delete(cache_key)


@pytest.mark.django_db
def test_calling_api_when_cache_for_projects_is_set(
    client, phase_factory, project_factory, django_assert_num_queries
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

    from freezegun import freeze_time

    with freeze_time(now):
        namespace = "projects-list"
        with django_assert_num_queries(0):
            # 0 number of queries means the api results are cached
            url = reverse(namespace) + "?status=activeParticipation"
            response = client.get(url)
            assert response.status_code == 200
            cache_active_projects = cache.get("projects_activeParticipation")
            assert response.data == cache_active_projects

            url = reverse(namespace) + "?status=futureParticipation"
            response = client.get(url)
            assert response.status_code == 200
            cache_future_projects = cache.get("projects_futureParticipation")
            assert response.data == cache_future_projects

            url = reverse(namespace) + "?status=pastParticipation"
            response = client.get(url)
            assert response.status_code == 200
            cache_past_projects = cache.get("projects_pastParticipation")
            assert response.data == cache_past_projects

            url = reverse(namespace)
            response = client.get(url)
            assert response.status_code == 200
            cache_projects = cache.get("projects_")
            assert response.data == cache_projects

        cache.delete_many(
            [
                "projects_",
                "projects_activeParticipation",
                "projects_futureParticipation",
                "projects_pastParticipation",
            ]
        )

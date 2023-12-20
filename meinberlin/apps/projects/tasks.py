from datetime import datetime
from datetime import timedelta
from datetime import timezone

from celery import shared_task
from django.core.cache import cache

from adhocracy4.phases.models import Phase
from meinberlin.apps import logger


def get_next_projects_start() -> list:
    """
    Helper function to query the db and retrieve the
    phases for projects that will start in the next 10min.

    Returns:
        A list with the phases timestamp and remaining seconds.
    """
    now = datetime.now(tz=timezone.utc)  # tz is UTC
    phases = (
        Phase.objects.filter(
            module__is_draft=False,
            start_date__isnull=False,
            start_date__range=[now, now + timedelta(minutes=10)],
        )
        .order_by("start_date")
        .all()
    )
    list_format_phases = []
    if phases:
        for phase in phases:
            # compare now with next start date
            phase_start_date = phase.start_date.astimezone(timezone.utc)
            remain_time = phase_start_date - now
            str_phase = phase_start_date.strftime("%Y-%m-%d, %H:%M:%S %Z")
            list_format_phases.append(
                (str_phase, remain_time.total_seconds(), "future")
            )

        # set the redis key: value
        cache.set("next_projects_start", list_format_phases)

    return list_format_phases


def get_next_projects_end() -> list:
    """
    Helper function to query the db and
    retrieve the earliest phase that will end.

    Returns:
        A list with the phases timestamp and remaining seconds.
    """
    now = datetime.now(tz=timezone.utc)  # tz is UTC
    phases = (
        Phase.objects.filter(
            module__is_draft=False,
            end_date__isnull=False,
            end_date__range=[now, now + timedelta(minutes=10)],
        )
        .order_by("end_date")
        .all()
    )

    list_format_phases = []
    if phases:
        for phase in phases:
            # compare now with next start date
            phase_end_date = phase.end_date.astimezone(timezone.utc)
            remain_time = phase_end_date - now
            str_phase = phase_end_date.strftime("%Y-%m-%d, %H:%M:%S %Z")
            list_format_phases.append(
                (str_phase, remain_time.total_seconds(), "active")
            )

        # set the redis key: value
        cache.set("next_projects_end", list_format_phases)

    return list_format_phases


@shared_task(name="schedule_reset_cache_for_projects")
def schedule_reset_cache_for_projects() -> bool:
    """The task is set via celery beat every 10 minutes in
    settings/production.txt.

    Returns:
        A boolean indicating if there are projects
        becoming past or active in the next 10 minutes
        and when the cache will be cleared.

        Task propagates a log info with a list
        of the phases timestamps.
    """

    msg = "Projects will be removed from cache: "
    success = False
    starts = False
    ends = False

    # check if redis has cache for past projects ending
    list_projects_end = cache.get("next_projects_end")
    if not list_projects_end:
        list_projects_end = get_next_projects_end()

    # check if redis has cache for future projects starting
    list_projects_start = cache.get("next_projects_start")
    if not list_projects_start:
        list_projects_start = get_next_projects_start()

    list_timestamps = list_projects_end + list_projects_start

    if list_timestamps:
        for timestamp in list_timestamps:
            project_phase = timestamp[0]
            remain_time = timestamp[1]
            project_status = timestamp[2]
            if project_status == "future":
                starts = True
            else:
                ends = True
            # schedule cache clear for the seconds between now and next end
            reset_cache_for_projects.apply_async([starts, ends], countdown=remain_time)
            msg = f"""
                    {project_status} {project_phase} in {remain_time/60} minutes
                    """
        success = True
    else:
        msg += "None"

    logger.info(msg)
    return success


@shared_task
def reset_cache_for_projects(starts: bool, ends: bool) -> str:
    """
    Task called by schedule_reset_cache_for_projects
    and clears cache for projects.

    Returns:
        A message indicating the participation
        status of the projects that the cache
        succeeded or failed to clear along with
        other relevant type of projects.
    """

    msg = "Clear cache "
    if starts:
        # remove redis key next_project_start
        cache.delete("next_projects_start")
        cache.delete_many(
            [
                "projects_activeParticipation",
                "projects_futureParticipation",
                "private_projects",
                "extprojects",
            ]
        )
        if cache.get_many(
            [
                "projects_activeParticipation",
                "projects_futureParticipation",
                "private_projects",
                "extprojects",
            ]
        ):
            msg += "failed for future projects becoming active"
        else:
            msg += "succeeded for future projects becoming active"
    if ends:
        # remove redis key next_projects_end
        cache.delete("next_projects_end")
        cache.delete_many(
            [
                "projects_activeParticipation",
                "projects_pastParticipation",
                "private_projects",
                "extprojects",
            ]
        )
        if cache.get_many(
            [
                "projects_activeParticipation",
                "projects_pastParticipation",
                "private_projects",
                "extprojects",
            ]
        ):
            msg += "failed for active projects becoming past"
        else:
            msg += "succeeded for active projects becoming past"
    logger.info(msg)
    return msg

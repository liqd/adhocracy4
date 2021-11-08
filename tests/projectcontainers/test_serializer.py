import pytest
from dateutil.parser import parse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from freezegun import freeze_time

from meinberlin.apps.projectcontainers.models import ProjectContainer
from meinberlin.apps.projectcontainers.serializers import \
    ProjectContainerSerializer


@pytest.mark.django_db
def test_projectcontainer_serializer(project_container_factory, phase_factory):

    pc_active = project_container_factory(name='active')
    project_active = pc_active.projects.first()

    pc_future = project_container_factory(name='future')
    project_future = pc_future.projects.first()

    pc_active_and_future = project_container_factory(name='active and future')
    project_active_and_future = pc_active_and_future.projects.first()

    pc_past = project_container_factory(name='past')
    project_past = pc_past.projects.first()

    now = parse('2013-01-01 18:00:00 UTC')
    yesterday = now - timezone.timedelta(days=1)
    last_week = now - timezone.timedelta(days=7)
    tomorrow = now + timezone.timedelta(days=1)
    next_week = now + timezone.timedelta(days=7)

    # active phase
    phase_factory(
        start_date=last_week,
        end_date=next_week,
        module__project=project_active,
    )

    # future phase
    phase_factory(
        start_date=tomorrow,
        end_date=next_week,
        module__project=project_future,
    )

    # active phase
    phase_factory(
        start_date=yesterday,
        end_date=tomorrow,
        module__project=project_active_and_future,
    )

    # future_phase
    phase_factory(
        start_date=tomorrow,
        end_date=next_week,
        module__project=project_active_and_future,
    )

    # past phase
    phase_factory(
        start_date=last_week,
        end_date=yesterday,
        module__project=project_past,
    )

    with freeze_time(now):
        containers = ProjectContainer.objects.all().order_by('created')
        data = ProjectContainerSerializer(containers, many=True, now=now).data
        assert len(data) == 4

        assert data[0]['type'] == 'project'
        assert data[1]['type'] == 'project'
        assert data[2]['type'] == 'project'
        assert data[3]['type'] == 'project'

        assert data[0]['subtype'] == 'container'
        assert data[1]['subtype'] == 'container'
        assert data[2]['subtype'] == 'container'
        assert data[3]['subtype'] == 'container'

        assert data[0]['published_projects_count'] == 1
        assert data[1]['published_projects_count'] == 1
        assert data[2]['published_projects_count'] == 1
        assert data[3]['published_projects_count'] == 1

        assert data[0]['title'] == 'active'
        assert data[1]['title'] == 'future'
        assert data[2]['title'] == 'active and future'
        assert data[3]['title'] == 'past'

        assert data[0]['participation_string'] == _('running')
        assert data[1]['participation_string'] == _('starts in the future')
        assert data[2]['participation_string'] == _('running')
        assert data[3]['participation_string'] == _('done')

        assert data[0]['status'] == 0
        assert data[1]['status'] == 0
        assert data[2]['status'] == 0
        assert data[3]['status'] == 1

        assert data[0]['participation_active']
        assert data[1]['participation_active']
        assert data[2]['participation_active']
        assert not data[3]['participation_active']

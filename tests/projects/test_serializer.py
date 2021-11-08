import pytest
from dateutil.parser import parse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from freezegun import freeze_time

from adhocracy4.projects.models import Project
from meinberlin.apps.projects.serializers import ProjectSerializer


@pytest.mark.django_db
def test_project_serializer(client, project_factory,
                            project_container_factory,
                            external_project_factory,
                            bplan_factory,
                            phase_factory):

    project_active = project_factory(name='active')
    project_future = project_factory(name='future')
    project_active_and_future = project_factory(name='active and future')
    project_past = project_factory(name='past')
    project_container_factory()
    external_project_factory()
    bplan_factory()

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

        projects = Project.objects.all().order_by('created')

        project_serializer = ProjectSerializer(projects, many=True, now=now)
        project_data = project_serializer.data
        assert len(project_data) == 8

        assert project_data[0]['type'] == 'project'
        assert project_data[1]['type'] == 'project'
        assert project_data[2]['type'] == 'project'
        assert project_data[3]['type'] == 'project'
        assert project_data[4]['type'] == 'project'
        assert project_data[5]['type'] == 'project'
        assert project_data[6]['type'] == 'project'
        assert project_data[7]['type'] == 'project'

        assert project_data[0]['subtype'] == 'default'
        assert project_data[1]['subtype'] == 'default'
        assert project_data[2]['subtype'] == 'default'
        assert project_data[3]['subtype'] == 'default'
        assert project_data[4]['subtype'] == 'container'
        assert project_data[5]['subtype'] == 'default'
        assert project_data[6]['subtype'] == 'external'
        assert project_data[7]['subtype'] == 'external'

        assert project_data[0]['title'] == 'active'
        assert project_data[1]['title'] == 'future'
        assert project_data[2]['title'] == 'active and future'
        assert project_data[3]['title'] == 'past'

        assert project_data[0]['participation_string'] == \
            _('running')
        assert project_data[1]['participation_string'] == \
            _('starts at {}').format(tomorrow.strftime('%d.%m.%Y'))
        assert project_data[2]['participation_string'] == \
            _('running')
        assert project_data[3]['participation_string'] == \
            _('done')

        assert project_data[0]['active_phase'][0] == 50
        assert '7' in project_data[0]['active_phase'][1]
        assert project_data[0]['active_phase'][2] == str(next_week)
        assert not project_data[1]['active_phase']
        assert project_data[2]['active_phase'][0] == 50
        assert '1' in project_data[2]['active_phase'][1]
        assert project_data[2]['active_phase'][2] == str(tomorrow)
        assert not project_data[3]['active_phase']
        assert not project_data[4]['active_phase']
        assert not project_data[5]['active_phase']

        assert not project_data[0]['future_phase']
        assert project_data[1]['future_phase'] == str(tomorrow)
        assert project_data[2]['future_phase'] == str(tomorrow)
        assert not project_data[3]['future_phase']
        assert not project_data[4]['future_phase']
        assert not project_data[5]['future_phase']

        assert not project_data[0]['past_phase']
        assert not project_data[1]['past_phase']
        assert not project_data[2]['past_phase']
        assert project_data[3]['past_phase'] == str(yesterday)
        assert not project_data[4]['past_phase']
        assert not project_data[5]['past_phase']

        assert project_data[0]['participation_active']
        assert project_data[1]['participation_active']
        assert project_data[2]['participation_active']
        assert not project_data[3]['participation_active']
        assert not project_data[4]['participation_active']
        assert not project_data[5]['participation_active']

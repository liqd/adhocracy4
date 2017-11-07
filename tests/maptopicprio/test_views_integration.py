import pytest

from meinberlin.apps.maptopicprio import phases
from tests.helpers import assert_template_response
from tests.helpers import freeze_phase
from tests.helpers import setup_phase


@pytest.mark.django_db
def test_list_view(client, phase_factory, maptopic_factory):
    phase, module, project, item = setup_phase(
        phase_factory, maptopic_factory, phases.PrioritizePhase)
    url = project.get_absolute_url()
    with freeze_phase(phase):
        response = client.get(url)
        assert_template_response(
            response, 'meinberlin_maptopicprio/maptopic_list.html')


@pytest.mark.django_db
def test_detail_view(client, phase_factory, maptopic_factory):
    phase, module, project, item = setup_phase(
        phase_factory, maptopic_factory, phases.PrioritizePhase)
    url = item.get_absolute_url()
    with freeze_phase(phase):
        response = client.get(url)
        assert_template_response(
            response, 'meinberlin_maptopicprio/maptopic_detail.html')

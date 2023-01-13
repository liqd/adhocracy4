import pytest

from adhocracy4.test.helpers import assert_template_response
from adhocracy4.test.helpers import freeze_phase
from adhocracy4.test.helpers import setup_phase
from meinberlin.apps.maptopicprio import phases


@pytest.mark.django_db
def test_list_view(client, phase_factory, maptopic_factory):
    phase, module, project, maptopic = setup_phase(
        phase_factory, maptopic_factory, phases.PrioritizePhase
    )
    phase_2, module_2, project_2, maptopic_2 = setup_phase(
        phase_factory, maptopic_factory, phases.PrioritizePhase
    )
    url = project.get_absolute_url()

    with freeze_phase(phase):
        response = client.get(url)
        assert_template_response(response, "meinberlin_maptopicprio/maptopic_list.html")
        assert maptopic in response.context_data["maptopic_list"]
        assert maptopic_2 not in response.context_data["maptopic_list"]
        assert response.context_data["maptopic_list"][0].comment_count == 0
        assert response.context_data["maptopic_list"][0].positive_rating_count == 0
        assert response.context_data["maptopic_list"][0].negative_rating_count == 0

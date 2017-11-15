import pytest

from meinberlin.apps.topicprio import phases
from meinberlin.test.helpers import assert_template_response
from meinberlin.test.helpers import freeze_phase
from meinberlin.test.helpers import setup_phase


@pytest.mark.django_db
def test_list_view(client, phase_factory, topic_factory):
    phase, module, project, item = setup_phase(
        phase_factory, topic_factory, phases.PrioritizePhase)
    url = project.get_absolute_url()
    with freeze_phase(phase):
        response = client.get(url)
        assert_template_response(
            response, 'meinberlin_topicprio/topic_list.html')


@pytest.mark.django_db
def test_detail_view(client, phase_factory, topic_factory):
    phase, module, project, item = setup_phase(
        phase_factory, topic_factory, phases.PrioritizePhase)
    url = item.get_absolute_url()
    with freeze_phase(phase):
        response = client.get(url)
        assert_template_response(
            response, 'meinberlin_topicprio/topic_detail.html')

import pytest

from meinberlin.apps.polls import phases
from tests.helpers import freeze_phase
from tests.helpers import setup_phase


@pytest.mark.django_db
def test_detail_view(client, phase_factory, poll_factory, question_factory,
                     choice_factory):
    phase, module, project, item = setup_phase(
        phase_factory, poll_factory, phases.VotingPhase)
    question = question_factory(poll=item)
    choice_factory(question=question)
    url = project.get_absolute_url()
    with freeze_phase(phase):
        response = client.get(url)
        assert response.status_code == 200
        assert response.template_name == \
            ['meinberlin_polls/poll_detail.html']

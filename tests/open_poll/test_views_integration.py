import pytest

from adhocracy4.open_poll import phases
from adhocracy4.test.helpers import assert_template_response
from adhocracy4.test.helpers import freeze_phase
from adhocracy4.test.helpers import setup_phase


@pytest.mark.django_db
def test_detail_view(
    client, phase_factory, poll_factory, question_factory, choice_factory
):
    phase, module, project, item = setup_phase(
        phase_factory, poll_factory, phases.VotingPhase
    )
    question = question_factory(poll=item)
    choice_factory(question=question)
    url = project.get_absolute_url()
    with freeze_phase(phase):
        response = client.get(url)
        assert_template_response(response, "a4open_poll/openpoll_detail.html")
        assert response.template_name[0] == "a4open_poll/openpoll_detail.html"
        assert response.context_data.get("view").phase == phase

import pytest

from adhocracy4.test.helpers import assert_template_response
from adhocracy4.test.helpers import freeze_phase
from adhocracy4.test.helpers import setup_phase
from meinberlin.apps.ideas import phases


@pytest.mark.django_db
def test_list_view(client, phase_factory, idea_factory):
    phase, module, project, idea = setup_phase(
        phase_factory, idea_factory, phases.FeedbackPhase
    )
    phase_2, module_2, project_2, idea_2 = setup_phase(
        phase_factory, idea_factory, phases.FeedbackPhase
    )
    url = project.get_absolute_url()

    with freeze_phase(phase):
        response = client.get(url)
        assert_template_response(response, "meinberlin_ideas/idea_list.html")
        assert idea in response.context_data["idea_list"]
        assert idea_2 not in response.context_data["idea_list"]
        assert response.context_data["idea_list"][0].comment_count == 0
        assert response.context_data["idea_list"][0].positive_rating_count == 0
        assert response.context_data["idea_list"][0].negative_rating_count == 0


@pytest.mark.django_db
def test_list_view_qs_gets_annotated(client, phase_factory, idea_factory):
    phase, module, project, idea = setup_phase(
        phase_factory, idea_factory, phases.FeedbackPhase
    )
    url = project.get_absolute_url()

    with freeze_phase(phase):
        response = client.get(url)
        annotated_idea = response.context_data["idea_list"][0]
        assert hasattr(annotated_idea, "comment_count")
        assert hasattr(annotated_idea, "positive_rating_count")
        assert hasattr(annotated_idea, "negative_rating_count")

        # test that qs still gets annotated for invalid filter values
        response = client.get(url + "?ordering=invalid_ordering")
        annotated_idea = response.context_data["idea_list"][0]
        assert hasattr(annotated_idea, "comment_count")
        assert hasattr(annotated_idea, "positive_rating_count")
        assert hasattr(annotated_idea, "negative_rating_count")

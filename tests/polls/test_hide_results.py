from datetime import timedelta

import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from adhocracy4.polls import phases


@pytest.mark.django_db
def test_hide_results_during_active_phase(
    apiclient,
    user_factory,
    poll_factory,
    question_factory,
    choice_factory,
    vote_factory,
    phase_factory,
):
    """While results are hidden and the phase is active, counts are zeroed."""
    poll = poll_factory()
    question = question_factory(poll=poll)
    choice = choice_factory(question=question)
    user = user_factory()
    vote_factory(choice=choice, creator=user)

    phase_content = phases.VotingPhase()
    phase_factory(
        phase_content=phase_content,
        module=poll.module,
        start_date=timezone.now(),
        end_date=timezone.now() + timedelta(days=1),
    )

    poll.hide_results_until_finished = True
    poll.save()

    url = reverse("polls-detail", kwargs={"pk": poll.pk})
    apiclient.force_authenticate(user=user)
    response = apiclient.get(url, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["hide_results_until_finished"] is True
    q_data = response.data["questions"][0]
    assert all(c["count"] == 0 for c in q_data["choices"])
    assert q_data["totalVoteCount"] == 0


@pytest.mark.django_db
def test_results_visible_after_phase_ends(
    apiclient,
    user_factory,
    poll_factory,
    question_factory,
    choice_factory,
    vote_factory,
    phase_factory,
):
    """Once the phase has ended, results are visible even with the setting on."""
    poll = poll_factory()
    question = question_factory(poll=poll)
    choice = choice_factory(question=question)
    user = user_factory()
    vote_factory(choice=choice, creator=user)

    # Default phase factory dates are in the past, so the phase has ended.
    phase_content = phases.VotingPhase()
    phase_factory(phase_content=phase_content, module=poll.module)

    poll.hide_results_until_finished = True
    poll.save()

    url = reverse("polls-detail", kwargs={"pk": poll.pk})
    apiclient.force_authenticate(user=user)
    response = apiclient.get(url, format="json")

    assert response.status_code == status.HTTP_200_OK
    q_data = response.data["questions"][0]
    assert q_data["choices"][0]["count"] == 1
    assert q_data["totalVoteCount"] == 1


@pytest.mark.django_db
def test_dashboard_save_hide_results(
    apiclient,
    admin,
    poll_factory,
    question_factory,
    choice_factory,
    phase_factory,
):
    """The dashboard can toggle the hide-results setting."""
    poll = poll_factory()
    question = question_factory(poll=poll)
    choice = choice_factory(question=question)

    url = reverse("polls-detail", kwargs={"pk": poll.pk})
    apiclient.force_authenticate(user=admin)

    data = {
        "questions": [
            {
                "id": question.id,
                "label": question.label,
                "help_text": "",
                "multiple_choice": False,
                "is_open": False,
                "is_confidential": False,
                "choices": [
                    {
                        "id": choice.pk,
                        "label": choice.label,
                        "is_other_choice": False,
                    }
                ],
                "answers": [],
            }
        ],
        "hide_results_until_finished": True,
    }

    response = apiclient.put(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["hide_results_until_finished"] is True
    poll.refresh_from_db()
    assert poll.hide_results_until_finished is True

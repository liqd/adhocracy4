import pytest
from django.urls import reverse
from rest_framework import status

from adhocracy4.polls.exports import PollExportView


@pytest.mark.django_db
def test_confidential_open_question_hides_other_users_answers(
    apiclient,
    user_factory,
    poll_factory,
    open_question_factory,
    answer_factory,
):
    poll = poll_factory()
    question = open_question_factory(poll=poll, is_confidential=True)
    user_a = user_factory()
    user_b = user_factory()
    answer_factory(question=question, creator=user_a, answer="secret from A")
    answer_factory(question=question, creator=user_b, answer="secret from B")

    url = reverse("polls-detail", kwargs={"pk": poll.pk})
    apiclient.force_authenticate(user=user_a)
    response = apiclient.get(url, format="json")

    assert response.status_code == status.HTTP_200_OK
    q_data = response.data["questions"][0]
    assert q_data["is_confidential"] is True
    assert len(q_data["answers"]) == 1
    assert q_data["answers"][0]["answer"] == "secret from A"
    assert q_data["totalAnswerCount"] == 2


@pytest.mark.django_db
def test_confidential_choice_question_hides_counts_and_other_answers(
    apiclient,
    user_factory,
    poll_factory,
    question_factory,
    other_choice_factory,
    choice_factory,
    vote_factory,
    other_vote_factory,
):
    poll = poll_factory()
    question = question_factory(poll=poll, is_confidential=True)
    choice_factory(question=question, label="Option A")
    choice_factory(question=question, label="Option B")
    other_choice_option = other_choice_factory(question=question)
    user_a = user_factory()
    user_b = user_factory()
    vote_a = vote_factory(choice=other_choice_option, creator=user_a)
    vote_b = vote_factory(choice=other_choice_option, creator=user_b)
    other_vote_factory(vote=vote_a, answer="other text A")
    other_vote_factory(vote=vote_b, answer="other text B")

    url = reverse("polls-detail", kwargs={"pk": poll.pk})
    apiclient.force_authenticate(user=user_a)
    response = apiclient.get(url, format="json")

    assert response.status_code == status.HTTP_200_OK
    q_data = response.data["questions"][0]
    assert all(choice["count"] == 0 for choice in q_data["choices"])
    assert len(q_data["other_choice_answers"]) == 1
    assert q_data["other_choice_answers"][0]["answer"] == "other text A"
    assert q_data["totalVoteCount"] == 2


@pytest.mark.django_db
def test_admin_can_save_confidential_flag(
    apiclient,
    admin,
    poll_factory,
    question_factory,
    choice_factory,
):
    poll = poll_factory()
    question = question_factory(poll=poll)
    choice1 = choice_factory(question=question)
    choice2 = choice_factory(question=question)

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
                "is_confidential": True,
                "choices": [
                    {
                        "id": choice1.pk,
                        "label": choice1.label,
                        "is_other_choice": False,
                    },
                    {
                        "id": choice2.pk,
                        "label": choice2.label,
                        "is_other_choice": False,
                    },
                ],
                "answers": [],
            }
        ]
    }

    response = apiclient.put(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK
    question.refresh_from_db()
    assert question.is_confidential is True


@pytest.mark.django_db
def test_confidential_export_includes_all_answers(
    poll_factory,
    open_question_factory,
    answer_factory,
    user_factory,
):
    poll = poll_factory()
    question = open_question_factory(poll=poll, is_confidential=True)
    user_a = user_factory()
    user_b = user_factory()
    answer_factory(question=question, creator=user_a, answer="export A")
    answer_factory(question=question, creator=user_b, answer="export B")

    export_view = PollExportView(kwargs={"module": poll.module})
    export_view.poll = poll
    export_view._init_export_data()

    rows = list(export_view.export_rows())
    assert len(rows) == 2
    answers_in_export = {row[1] for row in rows}
    assert answers_in_export == {"export A", "export B"}

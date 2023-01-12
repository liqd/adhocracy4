import pytest

from adhocracy4.polls.exports import PollCommentExportView
from adhocracy4.polls.exports import PollExportView
from adhocracy4.ratings.models import Rating


@pytest.mark.django_db
def test_poll_comment_export_view(poll, comment_factory, rating_factory):

    comment_1 = comment_factory(content_object=poll)
    comment_2 = comment_factory(content_object=comment_1)
    rating_factory(content_object=comment_1, value=Rating.POSITIVE)
    rating_factory(content_object=comment_2, value=Rating.NEGATIVE)

    comment_export_view = PollCommentExportView(kwargs={"module": poll.module})

    header = comment_export_view.get_header()
    assert header == [
        "ID",
        "Comment",
        "Created",
        "Link",
        "Creator",
        "Positive ratings",
        "Negative ratings",
        "Reply to Comment",
    ]

    queryset = comment_export_view.get_queryset()
    assert queryset.count() == 2
    assert comment_1 in queryset
    assert comment_2 in queryset

    assert comment_export_view.get_field_data(comment_1, "ratings_positive") == 1
    assert comment_export_view.get_field_data(comment_1, "ratings_negative") == 0
    assert comment_export_view.get_field_data(comment_2, "ratings_negative") == 1
    assert (
        comment_export_view.get_field_data(comment_2, "replies_to_comment")
        == comment_1.id
    )


@pytest.mark.django_db
def test_poll_export_view(
    poll,
    user,
    question_factory,
    choice_factory,
    vote_factory,
    other_vote_factory,
    answer_factory,
):

    choice_question = question_factory(poll=poll, multiple_choice=True, weight=1)
    open_question = question_factory(poll=poll, is_open=True, weight=2)
    choice1 = choice_factory(question=choice_question, weight=1)
    choice2 = choice_factory(question=choice_question, weight=2)
    choice_other = choice_factory(
        question=choice_question, is_other_choice=True, weight=3
    )
    vote_factory(choice=choice1, creator=user)
    other_vote = vote_factory(choice=choice_other, creator=user)
    other_vote_factory(vote=other_vote, answer="answer other choice")
    answer_factory(question=open_question, answer="open answer", creator=user)

    export_view = PollExportView(kwargs={"module": poll.module})

    header = export_view.get_header()
    identifier_other_choice = (
        "Q" + str(choice_question.id) + "_A" + str(choice_other.id)
    )
    identifier_other_choice_text = identifier_other_choice + "_text"
    assert identifier_other_choice in header
    assert identifier_other_choice_text in header
    assert "user" in header

    fields = export_view.get_fields()[0]
    assert (choice1, False) in fields
    assert not (choice1, True) in fields
    assert (choice_other, True) in fields
    assert (open_question, False) in fields
    assert (open_question, True) in fields

    assert export_view.get_object_list() == [(0, user)]

    assert export_view.get_field_data((0, user), (choice2, False)) == 0
    assert export_view.get_field_data((0, user), (choice_other, False)) == 1
    assert (
        export_view.get_field_data((0, user), (choice_other, True))
        == "answer other choice"
    )
    assert export_view.get_field_data((0, user), (open_question, False)) == 1
    assert export_view.get_field_data((0, user), (open_question, True)) == "open answer"

    rows = list(export_view.export_rows())
    assert rows[0] == [1, 1, 0, 1, "answer other choice", 1, "open answer"]

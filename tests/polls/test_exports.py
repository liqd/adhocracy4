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
def test_poll_export_with_data(
    poll_factory, question_factory, choice_factory, vote_factory, answer_factory, user
):
    poll = poll_factory()
    choice_question = question_factory(poll=poll, label="Rate this")
    open_question = question_factory(poll=poll, is_open=True, label="Comments")

    choice = choice_factory(question=choice_question, label="Good")

    # Create test data
    vote_factory(choice=choice, creator=user)
    answer_factory(question=open_question, creator=user, answer="Nice poll!")

    # Initialize export
    export_view = PollExportView(kwargs={"module": poll.module})
    export_view.poll = poll
    export_view._init_export_data()

    # Verify export
    rows = list(export_view.export_rows())
    assert len(rows) == 1
    assert rows[0] == [
        "1",  # Voter ID
        "Nice poll!",  # Open answer
        1,  # "Good" selected (1)
    ]

import uuid

import pytest

from adhocracy4.polls.exports import HumanReadablePollExportView
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


@pytest.mark.django_db
def test_human_readable_poll_export(
    poll_factory,
    question_factory,
    open_question_factory,
    choice_factory,
    other_choice_factory,
    vote_factory,
    other_vote_factory,
    answer_factory,
    user,
):
    poll = poll_factory()
    single_question = question_factory(
        poll=poll, label="Was gefällt ihnen im Park am besten?", weight=1
    )
    multi_question = question_factory(
        poll=poll,
        label="Was sollen wir noch zusätzlich zum Park hinzufügen?",
        multiple_choice=True,
        weight=2,
    )
    open_question = open_question_factory(
        poll=poll, label="Was möchten sie uns noch sagen?", weight=3
    )

    wiese = choice_factory(question=single_question, label="Wiese", weight=1)
    single_other = other_choice_factory(
        question=single_question, label="other", weight=2
    )

    spielplatz = choice_factory(question=multi_question, label="Spielplatz", weight=1)
    skatepark = choice_factory(question=multi_question, label="Skatepark", weight=2)
    multi_other = other_choice_factory(question=multi_question, label="other", weight=3)

    # A registered respondent with a single, multiple (incl. other) and open answer
    vote_factory(choice=wiese, creator=user)
    vote_factory(choice=spielplatz, creator=user)
    vote_factory(choice=skatepark, creator=user)
    multi_other_vote = vote_factory(choice=multi_other, creator=user)
    other_vote_factory(vote=multi_other_vote, answer="Käsetheke")
    answer_factory(question=open_question, creator=user, answer="Danke für die Umfrage")

    # An anonymous respondent with only a single "other" answer
    anon_single_other_vote = vote_factory(
        choice=single_other, creator=None, content_id=uuid.uuid4()
    )
    other_vote_factory(vote=anon_single_other_vote, answer="das wetter")

    export_view = HumanReadablePollExportView(kwargs={"module": poll.module})
    export_view._init_export_data()

    assert export_view.get_header() == [
        "Respondent",
        single_question.label,
        multi_question.label,
        open_question.label,
    ]

    rows = list(export_view.export_rows())
    assert rows == [
        [
            "Respondent 1",
            "Wiese",
            "Spielplatz, Skatepark, Other: Käsetheke",
            "Danke für die Umfrage",
        ],
        [
            "Anonymous 2",
            "Other: das wetter",
            "",
            "",
        ],
    ]

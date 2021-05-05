import pytest
from freezegun import freeze_time

from adhocracy4.filters.filters import DistinctOrderingWithDailyRandomFilter
from adhocracy4.ratings.models import Rating
from tests.apps.questions.models import Question


@pytest.mark.django_db
def test_distinct_ordering_daily_random(question_factory):
    questions = [question_factory() for i in range(5)]
    qs = Question.objects.all()

    with freeze_time('2020-01-01 00:00:00 UTC'):
        random_filter = DistinctOrderingWithDailyRandomFilter()
        random_qs = random_filter.filter(qs, ['dailyrandom'])

        assert random_qs[0] == questions[4]
        assert random_qs[1] == questions[3]
        assert random_qs[2] == questions[0]
        assert random_qs[3] == questions[2]
        assert random_qs[4] == questions[1]

    with freeze_time('2020-01-02 00:00:00 UTC'):
        random_filter = DistinctOrderingWithDailyRandomFilter()
        random_qs = random_filter.filter(qs, ['dailyrandom'])

        assert random_qs[0] == questions[4]
        assert random_qs[1] == questions[3]
        assert random_qs[2] == questions[2]
        assert random_qs[3] == questions[1]
        assert random_qs[4] == questions[0]

    with freeze_time('2020-01-03 00:00:00 UTC'):
        random_filter = DistinctOrderingWithDailyRandomFilter()
        random_qs = random_filter.filter(qs, ['dailyrandom'])

        assert random_qs[0] == questions[3]
        assert random_qs[1] == questions[1]
        assert random_qs[2] == questions[0]
        assert random_qs[3] == questions[2]
        assert random_qs[4] == questions[4]


@pytest.mark.django_db
def test_distinct_ordering(question_factory, comment_factory, rating_factory):
    questions = [question_factory() for i in range(5)]
    comment_factory(content_object=questions[1])
    comment_factory(content_object=questions[2])
    comment_factory(content_object=questions[2])
    rating_factory(content_object=questions[0], value=Rating.POSITIVE)
    rating_factory(content_object=questions[4], value=Rating.POSITIVE)
    rating_factory(content_object=questions[4], value=Rating.POSITIVE)

    qs = Question.objects.all()
    qs = qs.annotate_comment_count().annotate_positive_rating_count()

    filter = DistinctOrderingWithDailyRandomFilter(
        fields=(
            ('-created', 'newest'),
            ('-comment_count', 'comments'),
            ('-positive_rating_count', 'support'),
            ('title', 'title'),
        ),
        choices=[('dailyrandom', ('Daily random')),
                 ('comments', ('Most comments')),
                 ('support', ('Most support'))]
    )
    qs_comments = filter.filter(qs, ['comments'])
    assert qs_comments[0] == questions[2]
    assert qs_comments[1] == questions[1]

    qs_ratings = filter.filter(qs, ['support'])

    assert qs_ratings[0] == questions[4]
    assert qs_ratings[1] == questions[0]

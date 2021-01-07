from datetime import date

import pytest
from freezegun import freeze_time

from adhocracy4.filters.filters import DistinctOrderingFilter
from tests.apps.questions.models import Question


@pytest.mark.django_db
def test_random_distinct_ordering_no_seed(question_factory):
    questions = [question_factory() for i in range(5)]
    qs = Question.objects.all()

    random_filter = DistinctOrderingFilter()
    random_qs = random_filter.filter(qs, ['?'])

    assert random_qs[0] == questions[1]
    assert random_qs[1] == questions[3]
    assert random_qs[2] == questions[4]
    assert random_qs[3] == questions[2]
    assert random_qs[4] == questions[0]


@pytest.mark.django_db
def test_random_distinct_ordering_with_date(question_factory):
    questions = [question_factory() for i in range(5)]
    qs = Question.objects.all()

    with freeze_time('2020-01-01 00:00:00 UTC'):
        random_filter = DistinctOrderingFilter(random_seed=date.today())
        random_qs = random_filter.filter(qs, ['?'])

        assert random_qs[0] == questions[4]
        assert random_qs[1] == questions[3]
        assert random_qs[2] == questions[0]
        assert random_qs[3] == questions[2]
        assert random_qs[4] == questions[1]

    with freeze_time('2020-01-02 00:00:00 UTC'):
        random_filter = DistinctOrderingFilter(random_seed=date.today())
        random_qs = random_filter.filter(qs, ['?'])

        assert random_qs[0] == questions[4]
        assert random_qs[1] == questions[3]
        assert random_qs[2] == questions[2]
        assert random_qs[3] == questions[1]
        assert random_qs[4] == questions[0]

    with freeze_time('2020-01-03 00:00:00 UTC'):
        random_filter = DistinctOrderingFilter(random_seed=date.today())
        random_qs = random_filter.filter(qs, ['?'])

        assert random_qs[0] == questions[3]
        assert random_qs[1] == questions[1]
        assert random_qs[2] == questions[0]
        assert random_qs[3] == questions[2]
        assert random_qs[4] == questions[4]

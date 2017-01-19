import pytest

from tests.apps.questions import models


@pytest.mark.django_db
def test_annotate_ratings(question_factory, rating_factory):
    questions = [question_factory() for i in range(3)]
    rating_factory(content_object=questions[1], value=1)
    rating_factory(content_object=questions[1], value=1)
    rating_factory(content_object=questions[2], value=1)
    rating_factory(content_object=questions[2], value=-1)
    rating_factory(content_object=questions[2], value=-1)

    qs = models.Question.objects.annotate_positive_rating_count()
    assert qs.get(pk=questions[0].pk).positive_rating_count == 0
    assert qs.get(pk=questions[1].pk).positive_rating_count == 2
    assert qs.get(pk=questions[2].pk).positive_rating_count == 1
    qs = models.Question.objects.annotate_negative_rating_count()
    assert qs.get(pk=questions[0].pk).negative_rating_count == 0
    assert qs.get(pk=questions[1].pk).negative_rating_count == 0
    assert qs.get(pk=questions[2].pk).negative_rating_count == 2


@pytest.mark.django_db
def test_annotate_comment(question_factory, comment_factory):
    questions = [question_factory() for i in range(3)]
    comment_factory(content_object=questions[2])
    comment_factory(content_object=questions[1])
    comment_factory(content_object=questions[1])

    qs = models.Question.objects.annotate_comment_count()
    assert qs.get(pk=questions[0].pk).comment_count == 0
    assert qs.get(pk=questions[1].pk).comment_count == 2
    assert qs.get(pk=questions[2].pk).comment_count == 1


@pytest.mark.django_db
def test_combined_annotations(question, comment_factory, rating_factory):
    qs = models.Question.objects.annotate_comment_count() \
        .annotate_positive_rating_count()
    assert qs.first().comment_count == 0
    assert qs.first().positive_rating_count == 0

    comment_factory(content_object=question)
    rating_factory(content_object=question, value=1)
    rating_factory(content_object=question, value=1)

    qs = models.Question.objects.annotate_comment_count() \
        .annotate_positive_rating_count()
    assert qs.first().comment_count == 1
    assert qs.first().positive_rating_count == 2

    comment_factory(content_object=question)
    comment_factory(content_object=question)

    qs = models.Question.objects.annotate_comment_count() \
        .annotate_positive_rating_count()
    assert qs.first().comment_count == 3
    assert qs.first().positive_rating_count == 2

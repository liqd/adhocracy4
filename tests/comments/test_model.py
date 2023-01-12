from urllib.parse import urljoin

import pytest

from adhocracy4.comments import models as comments_models
from adhocracy4.ratings import models as rating_models


@pytest.mark.django_db
def test_delete_comment(comment_factory, rating_factory):
    comment = comment_factory()

    for i in range(5):
        comment_factory(content_object=comment)
    comment_count = comments_models.Comment.objects.all().count()

    rating_factory(content_object=comment)
    rating_count = rating_models.Rating.objects.all().count()

    assert comment_count == 6
    assert rating_count == 1

    comment.delete()

    comment_count = comments_models.Comment.objects.all().count()
    rating_count = rating_models.Rating.objects.all().count()
    assert comment_count == 0
    assert rating_count == 0


@pytest.mark.django_db
def test_save(comment_factory):
    comment_removed = comment_factory(comment="I am not yet removed")
    comment_censored = comment_factory(comment="I am not yet censored")
    comment_edited = comment_factory(comment="I am not yet edited")

    assert comment_removed.comment == "I am not yet removed"
    assert comment_censored.comment == "I am not yet censored"
    assert (
        comment_edited.comment
        == comment_edited._former_comment
        == "I am not yet edited"
    )

    comment_removed.is_removed = True
    comment_removed.save()
    comment_removed.refresh_from_db()
    comment_censored.is_censored = True
    comment_censored.save()
    comment_censored.refresh_from_db()
    comment_edited.comment = "I am edited"
    comment_edited.save()
    comment_edited.refresh_from_db()

    assert comment_removed.comment == comment_removed._former_comment == ""
    assert comment_censored.comment == comment_censored._former_comment == ""
    assert not comment_edited.comment == comment_edited._former_comment


@pytest.mark.django_db
def test_str(comment_factory):
    short_comment = comment_factory(comment="I am so short")
    long_comment = comment_factory(
        comment="I am a very very very long comment. More than 200 "
        "characters. Yes yes yes. That long! Really that long. How long is "
        "that. Yes yes yes. That long! Really that long. How long is that. "
        "Yes yes yes. That long! Really that long. How long is that."
    )

    assert str(short_comment) == short_comment.comment
    assert str(long_comment) == "{} ...".format(long_comment.comment[:200])


@pytest.mark.django_db
def test_get_absolute_url(comment, child_comment):
    # comment from factory has Question as content_object, which does not
    # define get_absolte_url, so url of module is used
    assert comment.get_absolute_url() == urljoin(
        comment.module.get_absolute_url(), "?comment={}".format(str(comment.id))
    )
    assert child_comment.get_absolute_url() == urljoin(
        child_comment.content_object.get_absolute_url(),
        "?comment={}".format(str(child_comment.id)),
    )


@pytest.mark.django_db
def test_notification_content(comment):
    assert comment.notification_content == comment.comment


@pytest.mark.django_db
def test_project(comment):
    assert comment.project == comment.module.project


@pytest.mark.django_db
def test_module(comment, child_comment):
    assert comment.module == comment.content_object.module
    assert child_comment.module == child_comment.content_object.content_object.module

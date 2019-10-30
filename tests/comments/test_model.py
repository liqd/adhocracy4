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

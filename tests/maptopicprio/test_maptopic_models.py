import os

import pytest
from django.conf import settings

from adhocracy4.comments import models as comments_models
from adhocracy4.ratings import models as rating_models
from adhocracy4.test.helpers import create_thumbnail
from meinberlin.apps.maptopicprio import models as idea_models


@pytest.mark.django_db
def test_delete_idea(maptopic_factory, comment_factory,
                     rating_factory, ImagePNG):
    idea = maptopic_factory(image=ImagePNG)
    image_path = os.path.join(settings.MEDIA_ROOT, idea.image.path)
    thumbnail_path = create_thumbnail(idea.image)

    for i in range(5):
        comment_factory(content_object=idea)
    comment_count = comments_models.Comment.objects.all().count()
    assert comment_count == len(idea.comments.all())

    rating_factory(content_object=idea)
    rating_count = rating_models.Rating.objects.all().count()

    assert os.path.isfile(image_path)
    assert os.path.isfile(thumbnail_path)
    count = idea_models.MapTopic.objects.all().count()
    assert count == 1
    assert comment_count == 5
    assert rating_count == 1

    idea.delete()
    assert not os.path.isfile(image_path)
    assert not os.path.isfile(thumbnail_path)
    count = idea_models.MapTopic.objects.all().count()
    comment_count = comments_models.Comment.objects.all().count()
    rating_count = rating_models.Rating.objects.all().count()
    assert count == 0
    assert comment_count == 0


@pytest.mark.django_db
def test_image_deleted_after_update(maptopic_factory, ImagePNG):
    idea = maptopic_factory(image=ImagePNG)
    image_path = os.path.join(settings.MEDIA_ROOT, idea.image.path)
    thumbnail_path = create_thumbnail(idea.image)

    assert os.path.isfile(image_path)
    assert os.path.isfile(thumbnail_path)

    idea.image = None
    idea.save()

    assert not os.path.isfile(image_path)
    assert not os.path.isfile(thumbnail_path)

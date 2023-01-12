from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models

from adhocracy4.categories.fields import CategoryField
from adhocracy4.comments.models import Comment
from adhocracy4.models.base import TimeStampedModel
from adhocracy4.models.query import CommentableQuerySet
from adhocracy4.models.query import RateableQuerySet
from adhocracy4.modules.models import Item
from adhocracy4.ratings.models import Rating


class QuestionQuerySet(CommentableQuerySet, RateableQuerySet):
    pass


class Question(Item):
    text = models.CharField(max_length=120, default="Can i haz cheezburger, pls?")

    comments = GenericRelation(
        Comment, related_query_name="question", object_id_field="object_pk"
    )

    ratings = GenericRelation(
        Rating, related_query_name="question", object_id_field="object_pk"
    )
    category = CategoryField()

    last_discussed = models.DateTimeField(blank=True, null=True, editable=False)

    objects = QuestionQuerySet.as_manager()


class TokenVote(TimeStampedModel):
    """Used in mB for the three phase Bürgerhaushalt."""

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_pk = models.PositiveIntegerField()
    content_object = GenericForeignKey(ct_field="content_type", fk_field="object_pk")

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from adhocracy4.comments.models import Comment
from adhocracy4.models.query import CommentableQuerySet
from adhocracy4.models.query import RatableQuerySet
from adhocracy4.modules.models import Item
from adhocracy4.ratings.models import Rating


class QuestionQuerySet(CommentableQuerySet, RatableQuerySet):
    pass


class Question(Item):
    text = models.CharField(max_length=120,
                            default='Can i haz cheezburger, pls?')

    comments = GenericRelation(Comment,
                               related_query_name='question',
                               object_id_field='object_pk')

    ratings = GenericRelation(Rating,
                              related_query_name='question',
                              object_id_field='object_pk')

    objects = QuestionQuerySet.as_manager()

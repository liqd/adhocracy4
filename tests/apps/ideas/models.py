from ckeditor.fields import RichTextField
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from adhocracy4.categories.fields import CategoryField
from adhocracy4.comments.models import Comment
from adhocracy4.maps import fields as map_fields
from adhocracy4.models.query import CommentableQuerySet
from adhocracy4.models.query import RateableQuerySet
from adhocracy4.modules.models import Item
from adhocracy4.ratings.models import Rating


class IdeaQuerySet(RateableQuerySet, CommentableQuerySet):
    pass


class Idea(Item):
    name = models.CharField(max_length=120,
                            default='Can i haz cheezburger, pls?')
    description = RichTextField(verbose_name='Description', blank=True)
    point = map_fields.PointField(blank=True)
    point_label = models.CharField(
        blank=True,
        default='',
        max_length=255,
        verbose_name='Label of the ideas location',
        help_text='This could be an address or the name of a landmark.',
    )
    comments = GenericRelation(Comment,
                               related_query_name='question',
                               object_id_field='object_pk')

    ratings = GenericRelation(Rating,
                              related_query_name='question',
                              object_id_field='object_pk')
    category = CategoryField()

    objects = IdeaQuerySet.as_manager()

    def get_absolute_url(self):
        return '/idea/%s/' % self.pk

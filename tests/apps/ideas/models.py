from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

from adhocracy4.categories.fields import CategoryField
from adhocracy4.comments.models import Comment
from adhocracy4.labels.models import Label
from adhocracy4.maps import fields as map_fields
from adhocracy4.models.query import CommentableQuerySet
from adhocracy4.models.query import RateableQuerySet
from adhocracy4.modules.models import Item
from adhocracy4.ratings.models import Rating
from tests.apps.moderatorfeedback.models import ModeratorFeedback


class IdeaQuerySet(RateableQuerySet, CommentableQuerySet):
    pass


class Idea(Item):
    name = models.CharField(max_length=120, default="Can i haz cheezburger, pls?")
    description = CKEditor5Field(verbose_name="Description", blank=True)
    moderator_status = models.CharField(max_length=256, blank=True)
    moderator_feedback_text = models.OneToOneField(
        ModeratorFeedback,
        related_name="+",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )

    point = map_fields.PointField(blank=True)
    point_label = models.CharField(
        blank=True,
        default="",
        max_length=255,
        verbose_name="Label of the ideas location",
        help_text="This could be an address or the name of a landmark.",
    )
    comments = GenericRelation(
        Comment, related_query_name="question", object_id_field="object_pk"
    )

    ratings = GenericRelation(
        Rating, related_query_name="question", object_id_field="object_pk"
    )
    category = CategoryField()

    labels = models.ManyToManyField(
        Label, related_name=("%(app_label)s_" "%(class)s_label")
    )
    is_bool_test = models.BooleanField(default=True)

    objects = IdeaQuerySet.as_manager()

    def get_absolute_url(self):
        return "/idea/%s/" % self.pk

    @property
    def reference_number(self):
        return "{:d}-{:05d}".format(self.created.year, self.pk)

    def get_moderator_status_display(self):
        return self.moderator_status[1]

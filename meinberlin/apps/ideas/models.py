from autoslug import AutoSlugField
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.humanize.templatetags.humanize import intcomma
from django.db import models
from django.db.models.functions import Concat
from django.db.models.functions import ExtractYear
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.fields import CKEditor5Field

from adhocracy4 import transforms
from adhocracy4.categories.fields import CategoryField
from adhocracy4.comments import models as comment_models
from adhocracy4.images.fields import ConfiguredImageField
from adhocracy4.labels import models as labels_models
from adhocracy4.models import query
from adhocracy4.modules import models as module_models
from adhocracy4.ratings import models as rating_models
from meinberlin.apps.moderatorfeedback.models import Moderateable
from meinberlin.apps.moderatorremark import models as remark_models

BADGES_LIMIT = 3


class IdeaQuerySet(query.RateableQuerySet, query.CommentableQuerySet):
    def annotate_reference_number(self):
        return self.annotate(
            ref_number=models.Case(
                models.When(
                    pk__lte=9,
                    then=Concat(
                        ExtractYear("created"),
                        models.Value("-0000"),
                        "pk",
                        output_field=models.CharField(),
                    ),
                ),
                models.When(
                    pk__lte=99,
                    then=Concat(
                        ExtractYear("created"),
                        models.Value("-000"),
                        "pk",
                        output_field=models.CharField(),
                    ),
                ),
                models.When(
                    pk__lte=999,
                    then=Concat(
                        ExtractYear("created"),
                        models.Value("-00"),
                        "pk",
                        output_field=models.CharField(),
                    ),
                ),
                models.When(
                    pk__lte=9999,
                    then=Concat(
                        ExtractYear("created"),
                        models.Value("-0"),
                        "pk",
                        output_field=models.CharField(),
                    ),
                ),
                default=Concat(
                    ExtractYear("created"),
                    models.Value("-"),
                    "pk",
                    output_field=models.CharField(),
                ),
            )
        )


class ItemBadgesPropertyMixin:
    """Use with idea items to display badges in list and detail view."""

    @property
    def item_badges(self):
        """List all badges an idea item can have."""
        labels = []
        if hasattr(self, "moderator_status") and self.moderator_status:
            labels.append(
                [
                    "moderator_status",
                    self.get_moderator_status_display(),
                    self.moderator_status,
                ]
            )
        if hasattr(self, "budget"):
            if self.budget == 0:
                labels.append(["budget", _("budget not specified")])
            else:
                labels.append(["budget", intcomma(self.budget) + "€"])
        if hasattr(self, "point_label") and self.point_label:
            labels.append(["point_label", self.point_label])
        if hasattr(self, "category") and self.category:
            labels.append(["category", self.category.name])
        if hasattr(self, "labels") and self.labels:
            for label in self.labels.all():
                labels.append(["label", label.name])
        return labels

    @property
    def item_badges_for_detail(self):
        item_badges_for_detail = [
            badge for badge in self.item_badges if badge[0] != "moderator_status"
        ]
        return item_badges_for_detail

    @property
    def item_badges_for_list(self):
        return self.item_badges[:BADGES_LIMIT]

    @property
    def additional_item_badges_for_list_count(self):
        count = 0
        if len(self.item_badges) > BADGES_LIMIT:
            count = len(self.item_badges) - BADGES_LIMIT
        return count


class AbstractIdea(module_models.Item, Moderateable, ItemBadgesPropertyMixin):
    item_ptr = models.OneToOneField(
        to=module_models.Item,
        parent_link=True,
        related_name="%(app_label)s_%(class)s",
        on_delete=models.CASCADE,
    )
    slug = AutoSlugField(populate_from="name", unique=True)
    name = models.CharField(max_length=120, verbose_name=_("Title"))
    description = CKEditor5Field(verbose_name=_("Description"))
    image = ConfiguredImageField(
        "idea_image",
        verbose_name=_("Add image"),
        upload_to="ideas/images",
        blank=True,
        help_prefix=_("Visualize your idea."),
    )
    category = CategoryField()

    labels = models.ManyToManyField(
        labels_models.Label,
        verbose_name=_("Labels"),
        related_name=("%(app_label)s_" "%(class)s_label"),
    )

    objects = IdeaQuerySet.as_manager()

    @property
    def reference_number(self):
        return "{:d}-{:05d}".format(self.created.year, self.pk)

    @property
    def remark(self):
        content_type = ContentType.objects.get_for_model(self)
        return remark_models.ModeratorRemark.objects.filter(
            item_content_type=content_type, item_object_id=self.id
        ).first()

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    def save(self, update_fields=None, *args, **kwargs):
        self.description = transforms.clean_html_field(self.description)
        if update_fields:
            update_fields = {"description"}.union(update_fields)
        super().save(update_fields=update_fields, *args, **kwargs)


class Idea(AbstractIdea):
    ratings = GenericRelation(
        rating_models.Rating, related_query_name="idea", object_id_field="object_pk"
    )
    comments = GenericRelation(
        comment_models.Comment, related_query_name="idea", object_id_field="object_pk"
    )

    def get_absolute_url(self):
        return reverse(
            "meinberlin_ideas:idea-detail",
            kwargs=dict(pk="{:05d}".format(self.pk), year=self.created.year),
        )

    class Meta:
        ordering = ["-created"]

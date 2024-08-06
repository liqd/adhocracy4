from urllib.parse import urljoin

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.translation import pgettext_lazy

from adhocracy4 import transforms
from adhocracy4.models import base
from adhocracy4.models.query import RateableQuerySet
from adhocracy4.projects.models import Project
from adhocracy4.ratings import models as rating_models
from adhocracy4.reports import models as report_models


class RateableCommentQuerySet(RateableQuerySet):
    pass


class Comment(base.UserGeneratedContentModel):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_pk = models.PositiveIntegerField()
    content_object = GenericForeignKey(ct_field="content_type", fk_field="object_pk")
    comment = models.TextField(max_length=4000)
    # true if deleted by creator, comment text is set to ''
    is_removed = models.BooleanField(default=False)
    # true if deleted by moderator/initiator/admin, comment text is set to ''
    is_censored = models.BooleanField(default=False)
    # true if blocked by moderator, comment text is kept, but not shown in discussion
    is_blocked = models.BooleanField(default=False)
    ratings = GenericRelation(
        rating_models.Rating, related_query_name="comment", object_id_field="object_pk"
    )
    reports = GenericRelation(
        report_models.Report, related_query_name="comment", object_id_field="object_pk"
    )
    child_comments = GenericRelation(
        "self", related_query_name="parent_comment", object_id_field="object_pk"
    )
    comment_categories = models.CharField(blank=True, max_length=256)
    last_discussed = models.DateTimeField(blank=True, null=True, editable=False)
    is_moderator_marked = models.BooleanField(default=False)
    # used in moderation dashboard, indicates if comment is marked as read by moderator
    is_reviewed = models.BooleanField(default=False)
    project = models.ForeignKey(
        Project, on_delete=models.SET_NULL, blank=True, null=True
    )

    objects = RateableCommentQuerySet.as_manager()

    class Meta:
        verbose_name = pgettext_lazy("noun", "Comment")
        verbose_name_plural = _("Comments")
        ordering = ("created",)
        indexes = [models.Index(fields=["content_type", "object_pk"])]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # save former comment to detect if comment text has changed
        self._former_comment = transforms.clean_html_all(self.comment)

    def __str__(self):
        if len(self.comment) > 200:
            return "{} ...".format(self.comment[:200])
        else:
            return "{}".format(self.comment)

    def save(self, update_fields=None, *args, **kwargs):
        """Change comment.comment if comment was marked removed or censored."""
        self.comment = transforms.clean_html_all(self.comment)
        update_project = False
        if not self.project:
            self.project = self.content_object.module.project
            update_project = True

        if self.is_removed or self.is_censored:
            self.comment = self._former_comment = ""
            self.comment_categories = ""

        if update_fields:
            update_fields = {"comment"}.union(update_fields)
            if update_project:
                update_fields = {"project"}.union(update_fields)

        super().save(update_fields=update_fields, *args, **kwargs)

    def get_absolute_url(self):
        if hasattr(self.content_object, "get_absolute_url"):
            return urljoin(
                self.content_object.get_absolute_url(),
                "?comment={}".format(str(self.id)),
            )
        else:
            return urljoin(
                self.module.get_absolute_url(), "?comment={}".format(str(self.id))
            )

    @property
    def notification_content(self):
        return self.comment

    @property
    def module(self):
        co = self.content_object
        if isinstance(co, self.__class__):
            co = co.content_object
        return co.module

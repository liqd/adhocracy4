from django.conf import settings
from django.contrib.auth.models import Group
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.fields import CKEditor5Field

from adhocracy4 import transforms
from adhocracy4.administrative_districts.models import AdministrativeDistrict
from adhocracy4.images.fields import ConfiguredImageField
from adhocracy4.images.fields import ImageAltTextField
from adhocracy4.images.fields import ImageCopyrightField
from adhocracy4.images.validators import ImageAltTextValidator
from adhocracy4.maps import fields as map_fields
from adhocracy4.models.base import UserGeneratedContentModel
from adhocracy4.phases.models import Phase
from adhocracy4.projects import models as project_models
from adhocracy4.projects.enums import Access
from adhocracy4.projects.models import ProjectContactDetailMixin
from adhocracy4.projects.models import Topic


class Plan(ProjectContactDetailMixin, UserGeneratedContentModel):
    PARTICIPATION_INFORMATION = 0
    PARTICIPATION_CONSULTATION = 1
    PARTICIPATION_COOPERATION = 2
    PARTICIPATION_DECISION_MAKING = 3
    PARTICIPATION_CHOICES = (
        (PARTICIPATION_INFORMATION, _("information (no participation)")),
        (PARTICIPATION_CONSULTATION, _("consultation")),
        (PARTICIPATION_COOPERATION, _("cooperation")),
        (PARTICIPATION_DECISION_MAKING, _("decision-making")),
    )

    STATUS_ONGOING = 0
    STATUS_DONE = 1

    STATUS_CHOICES = ((STATUS_ONGOING, _("running")), (STATUS_DONE, _("done")))

    title = models.CharField(
        max_length=120,
        verbose_name=_("Title of your plan"),
    )
    organisation = models.ForeignKey(
        settings.A4_ORGANISATIONS_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_("Organisation"),
    )
    projects = models.ManyToManyField(
        project_models.Project, related_name="plans", blank=True
    )
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, blank=True, null=True)
    point = map_fields.PointField(
        blank=True,
        verbose_name=_("Can your plan be located on the map?"),
    )
    point_label = models.CharField(
        blank=True,
        default="",
        max_length=255,
        verbose_name=_("Name of the site"),
    )
    district = models.ForeignKey(
        AdministrativeDistrict,
        verbose_name=_("District"),
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    cost = models.CharField(
        max_length=255,
        verbose_name=_("Cost"),
    )
    description = CKEditor5Field(
        config_name="collapsible-image-editor",
        verbose_name=_("Description of your plan"),
        validators=[ImageAltTextValidator()],
    )
    image = ConfiguredImageField(
        "plan_image",
        verbose_name=_("Header image"),
        upload_to="plan/description_image",
        blank=True,
        help_prefix=_("Visualize your plan with an image underneath the description."),
    )
    image_alt_text = ImageAltTextField(image_name=_("Header image"))
    image_copyright = models.CharField(
        verbose_name=_("Header image copyright"),
        blank=True,
        max_length=120,
    )
    tile_image = ConfiguredImageField(
        "tileimage",
        verbose_name=_("Tile image"),
        help_prefix=_("The image will be shown in the project tile."),
        upload_to="plan/tile_images",
        blank=True,
    )
    tile_image_alt_text = ImageAltTextField(image_name=_("Tile image"))
    tile_image_copyright = ImageCopyrightField(
        verbose_name=_("Tile image copyright"),
    )
    topics = models.ManyToManyField(
        Topic,
        verbose_name=_("Topics"),
    )
    status = models.SmallIntegerField(
        choices=STATUS_CHOICES,
        verbose_name=_("Status"),
    )
    participation = models.SmallIntegerField(
        choices=PARTICIPATION_CHOICES,
        default=PARTICIPATION_INFORMATION,
        verbose_name=_("Level of participation"),
    )
    participation_explanation = models.TextField(
        verbose_name=_("Participation explanation"),
        max_length=4000,
    )
    duration = models.CharField(
        blank=True,
        null=True,
        max_length=255,
        verbose_name=_("Duration"),
    )
    is_draft = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created"]

    @property
    def reference_number(self):
        return "{:d}-{:05d}".format(self.created.year, self.pk)

    @property
    def administrative_district(self):
        return self.district

    @property
    def topic_names(self):
        return [str(topic) for topic in self.topics.all()]

    @cached_property
    def published_projects(self):
        return self.projects.filter(
            Q(access=Access.PUBLIC) | Q(access=Access.SEMIPUBLIC),
            is_draft=False,
            is_archived=False,
        )

    @cached_property
    def participation_string(self):
        project_list = self.published_projects.values_list("id", flat=True)
        phases_in_plan = (
            Phase.objects.select_related("module__project")
            .filter(module__project_id__in=project_list)
            .order_by("-start_date")
        )

        if phases_in_plan.active_phases():
            return _("running")

        future_phases_with_start_date = phases_in_plan.future_phases().exclude(
            start_date__isnull=True
        )

        if future_phases_with_start_date:
            future_phase = future_phases_with_start_date.first()
            return _("starts at {}").format(
                future_phase.start_date.strftime("%d.%m.%Y")
            )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            "meinberlin_plans:plan-detail",
            kwargs=dict(pk="{:05d}".format(self.pk), year=self.created.year),
        )

    def save(self, update_fields=None, *args, **kwargs):
        self.description = transforms.clean_html_field(
            self.description, "collapsible-image-editor"
        )
        if update_fields:
            update_fields = {"description"}.union(update_fields)
        super().save(update_fields=update_fields, *args, **kwargs)

    def _get_group(self, user, organisation):
        user_groups = user.groups.all()
        org_groups = organisation.groups.all()
        shared_groups = user_groups & org_groups
        return shared_groups.distinct().first()

    def is_group_member(self, user):
        if self.group:
            return user.groups.filter(id=self.group.id).exists()
        return False

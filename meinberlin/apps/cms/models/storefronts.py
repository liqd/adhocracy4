import random

from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.functional import cached_property
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin import panels
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet

from adhocracy4.comments.models import Comment
from adhocracy4.modules.models import Item
from adhocracy4.projects.enums import Access
from adhocracy4.projects.models import Project
from meinberlin.apps.plans.models import Plan


def project_choice_limit():
    """Return project that are either active or are currently chosen (and possibly finished in meantime)"""
    now = timezone.now()
    chosen_projects = StorefrontItem.objects.values("project__id")
    limit_ids = Project.objects.filter(
        Q(is_draft=False, is_archived=False, module__phase__end_date__gte=now)
        | Q(id__in=chosen_projects)
    ).values_list("id", flat=True)
    limit = {"id__in": limit_ids}
    return limit


class StorefrontItem(models.Model):
    district = models.ForeignKey(
        "a4administrative_districts.AdministrativeDistrict",
        related_name="+",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    project = models.ForeignKey(
        "a4projects.Project",
        related_name="+",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        limit_choices_to=project_choice_limit,
    )
    quote = models.TextField(blank=True, max_length=150)
    district_project_count = models.PositiveIntegerField()

    def __str__(self):
        return str(self.pk)

    @cached_property
    def item_type(self):
        if self.project.project_type in (
            "meinberlin_extprojects.ExternalProject",
            "meinberlin_bplan.Bplan",
        ):
            return "external"
        return "project"

    @cached_property
    def project_url(self):
        if self.item_type == "external":
            return self.project.externalproject.url
        return self.project.get_absolute_url()

    def get_district_project_count(self):
        projects = Project.objects.filter(
            Q(access=Access.PUBLIC) | Q(access=Access.SEMIPUBLIC),
            administrative_district=self.district,
            is_draft=False,
            is_archived=False,
        )
        plans = Plan.objects.filter(
            district=self.district,
            status=0,
            is_draft=False,
        )
        active_project_count = plans.count()
        for project in projects:
            if project.active_phase_ends_next or project.future_phases:
                active_project_count += 1
        return active_project_count

    def save(self, *args, **kwargs):
        if not self.district_project_count:
            self.district_project_count = self.get_district_project_count()
        super().save(*args, **kwargs)

    panels = [
        FieldPanel("district"),
        FieldPanel("project"),
        FieldPanel("quote"),
    ]


def get_num_entries_count():
    num_comments = Comment.objects.all().count()
    num_items = Item.objects.all().count()
    return num_comments + num_items


def get_num_projects_count():
    projects = Project.objects.all().filter(
        Q(access=Access.PUBLIC) | Q(access=Access.SEMIPUBLIC),
        is_draft=False,
        is_archived=False,
    )
    active_project_count = 0
    for project in projects:
        if project.active_phase_ends_next or project.future_phases:
            active_project_count += 1
    return active_project_count


@register_snippet
class Storefront(ClusterableModel):
    title = models.CharField(max_length=255, null=False, blank=False)
    image = models.ForeignKey(
        "meinberlin_cms.CustomImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    teaser = models.CharField(max_length=100)
    num_entries = models.PositiveIntegerField(default=get_num_entries_count)
    num_projects = models.PositiveIntegerField(default=get_num_projects_count)

    def __str__(self):
        return self.title

    @cached_property
    def random_items(self):
        items = self.items.all()
        if items.count() > 3:
            items_list = items.values_list("id", flat=True)
            random_items = random.sample(list(items_list), 3)
            return StorefrontItem.objects.filter(id__in=random_items)
        else:
            return items

    title_panel = [panels.FieldPanel("title")]

    image_tile_panel = [panels.FieldPanel("image"), panels.FieldPanel("teaser")]

    project_tiles_panel = [panels.InlinePanel("items", min_num=3)]

    edit_handler = panels.TabbedInterface(
        [
            panels.ObjectList(title_panel, heading="Title"),
            panels.ObjectList(image_tile_panel, heading="Image Tile"),
            panels.ObjectList(project_tiles_panel, heading="Project Tiles"),
        ]
    )


class StorefrontCollection(StorefrontItem):
    parent = ParentalKey("meinberlin_cms.Storefront", related_name="items")

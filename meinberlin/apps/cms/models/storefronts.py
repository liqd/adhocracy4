import random

from django.db import models
from django.db.models import Q
from django.utils.functional import cached_property
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin import edit_handlers
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet

from adhocracy4.comments.models import Comment
from adhocracy4.modules.models import Item
from adhocracy4.projects.enums import Access
from adhocracy4.projects.models import Project
from meinberlin.apps.plans.models import Plan
from meinberlin.apps.projects import get_project_type


class StorefrontItem(models.Model):
    district = models.ForeignKey(
        'a4administrative_districts.AdministrativeDistrict',
        related_name='+',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    project = models.ForeignKey(
        'a4projects.Project',
        related_name='+',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    quote = models.TextField(
        blank=True,
        max_length=150
    )

    def __str__(self):
        return str(self.pk)

    @cached_property
    def item_type(self):
        if get_project_type(self.project) in ('external', 'bplan'):
            return 'external'
        return 'project'

    @cached_property
    def project_url(self):
        if self.item_type == 'external':
            return self.project.externalproject.url
        return self.project.get_absolute_url()

    @cached_property
    def district_project_count(self):
        projects = Project.objects\
            .filter(Q(access=Access.PUBLIC) | Q(access=Access.SEMIPUBLIC),
                    administrative_district=self.district,
                    is_draft=False,
                    is_archived=False
                    )
        plans = Plan.objects\
            .filter(district=self.district,
                    status=0
                    )
        active_project_count = plans.count()
        for project in projects:
            if project.active_phase or project.future_phases:
                active_project_count += 1
        return active_project_count

    panels = [
        FieldPanel('district'),
        FieldPanel('project'),
        FieldPanel('quote'),
    ]


@register_snippet
class Storefront(ClusterableModel):
    title = models.CharField(max_length=255, null=False, blank=False)
    image = models.ForeignKey(
        'meinberlin_cms.CustomImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    teaser = models.CharField(max_length=100)

    def __str__(self):
        return self.title

    @cached_property
    def num_entries(self):
        num_comments = Comment.objects.all().count()
        num_items = Item.objects.all().count()
        return num_comments + num_items

    @cached_property
    def num_projects(self):
        projects = Project.objects.all().filter(
            Q(access=Access.PUBLIC) | Q(access=Access.SEMIPUBLIC),
            is_draft=False, is_archived=False)
        active_project_count = 0
        for project in projects:
            if project.active_phase or project.future_phases:
                active_project_count += 1
        return active_project_count

    @cached_property
    def random_items(self):
        items = self.items.all()
        if items.count() > 3:
            items_list = items.values_list('id', flat=True)
            random_items = random.sample(list(items_list), 3)
            return StorefrontItem.objects.filter(id__in=random_items)
        else:
            return items

    title_panel = [
        edit_handlers.FieldPanel('title')
    ]

    image_tile_panel = [
        ImageChooserPanel('image'),
        edit_handlers.FieldPanel('teaser')
    ]

    project_tiles_panel = [
        edit_handlers.InlinePanel('items', min_num=3)
    ]

    edit_handler = edit_handlers.TabbedInterface([
        edit_handlers.ObjectList(title_panel, heading='Title'),
        edit_handlers.ObjectList(image_tile_panel, heading='Image Tile'),
        edit_handlers.ObjectList(project_tiles_panel, heading='Project Tiles')
    ])


class StorefrontCollection(StorefrontItem):
    parent = ParentalKey('meinberlin_cms.Storefront', related_name='items')

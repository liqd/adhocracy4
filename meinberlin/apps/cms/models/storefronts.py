import random

from django.db import models
from django.utils.functional import cached_property
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.wagtailadmin import edit_handlers
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsnippets.models import register_snippet


class StorefrontItem(models.Model):
    district = models.ForeignKey(
        'a4administrative_districts.AdministrativeDistrict',
        related_name='+',
        null=True,
        blank=True
    )
    project = models.ForeignKey(
        'a4projects.Project',
        related_name='+',
        null=True,
        blank=True
    )
    quote = models.TextField(
        blank=True,
        max_length=150
    )

    def __str__(self):
        return str(self.pk)

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

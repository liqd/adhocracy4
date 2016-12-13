from django.db import models
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailadmin.edit_handlers import InlinePanel
from wagtail.wagtailadmin.edit_handlers import PageChooserPanel
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.models import Orderable
from wagtail.wagtailcore.models import Page
from wagtail.wagtailsnippets.models import register_snippet


class HomePage(Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full")
    ]


class MenuItem(models.Model):
    title = models.CharField(max_length=255)
    link_page = models.ForeignKey('wagtailcore.Page')

    @property
    def url(self):
        return self.link_page.url

    def __str__(self):
        return self.title

    panels = [
        FieldPanel('title'),
        PageChooserPanel('link_page')
    ]


@register_snippet
class NavigationMenu(ClusterableModel):
    title = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return self.title

    panels = [
        FieldPanel('title'),
        InlinePanel('items')
    ]


class NavigationMenuItem(Orderable, MenuItem):
    parent = ParentalKey('cms.NavigationMenu', related_name='items')

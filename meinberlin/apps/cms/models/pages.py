from django.db import models
from wagtail.admin import edit_handlers
from wagtail.core import blocks
from wagtail.core import fields
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel

from meinberlin.apps.actions import blocks as actions_blocks
from meinberlin.apps.cms import blocks as cms_blocks


class SimplePage(Page):
    body = fields.RichTextField(blank=True)

    content_panels = [
        edit_handlers.FieldPanel('title'),
        edit_handlers.FieldPanel('body'),
    ]

    subpage_types = []


class StreamfieldSimplePage(Page):
    body = fields.StreamField([
        ('paragraph', blocks.RichTextBlock()),
        ('html', blocks.RawHTMLBlock())
    ], blank=True)

    content_panels = [
        edit_handlers.FieldPanel('title'),
        edit_handlers.StreamFieldPanel('body'),
    ]

    subpage_types = []


class HomePage(Page):
    body = fields.StreamField([
        ('paragraph', blocks.RichTextBlock(
            template='meinberlin_cms/blocks/richtext_block.html'
        )),
        ('call_to_action', cms_blocks.CallToActionBlock()),
        ('image_call_to_action', cms_blocks.ImageCallToActionBlock()),
        ('columns_text', cms_blocks.ColumnsBlock()),
        ('activities', actions_blocks.PlatformActivityBlock()),
        ('accordion', cms_blocks.DocsBlock()),
        ('infographic', cms_blocks.InfographicBlock()),
        ('map_teaser', cms_blocks.MapTeaserBlock())
    ])

    subtitle = models.CharField(max_length=120)

    header_image = models.ForeignKey(
        'meinberlin_cms.CustomImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    storefront = models.ForeignKey(
        'meinberlin_cms.Storefront',
        on_delete=models.SET_NULL,
        null=True,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        edit_handlers.FieldPanel('subtitle'),
        ImageChooserPanel('header_image'),
        edit_handlers.StreamFieldPanel('body'),
        SnippetChooserPanel('storefront')
    ]


class DocsPage(Page):
    body = fields.StreamField([
        ('documents_list', cms_blocks.DocsBlock()),
        ('header', blocks.CharBlock(
            template='meinberlin_cms/blocks/header.html'))
    ])

    description = fields.RichTextField(blank=True)

    content_panels = Page.content_panels + [
        edit_handlers.FieldPanel('description'),
        edit_handlers.StreamFieldPanel('body'),
    ]

    class Meta:
        verbose_name = 'Documents'

    subpage_types = []

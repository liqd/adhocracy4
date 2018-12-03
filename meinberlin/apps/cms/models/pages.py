from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin import edit_handlers
from wagtail.contrib.forms.models import AbstractEmailForm
from wagtail.contrib.forms.models import AbstractFormField
from wagtail.core import blocks
from wagtail.core import fields
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel

from meinberlin.apps.actions import blocks as actions_blocks
from meinberlin.apps.cms import blocks as cms_blocks
from meinberlin.apps.cms import emails


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
        ('projects', cms_blocks.ProjectsWrapperBlock()),
        ('activities', actions_blocks.PlatformActivityBlock()),
        ('accordion', cms_blocks.DocsBlock())
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


class EmailFormField(AbstractFormField):
    page = ParentalKey('EmailFormPage', related_name='form_fields')


class EmailFormPage(AbstractEmailForm):
    intro = fields.RichTextField(
        help_text='Introduction text shown above the form'
    )
    thank_you = fields.RichTextField(
        help_text='Text shown after form submission',
    )
    email_content = models.CharField(
        max_length=200,
        help_text='Email content message',
    )
    attach_as = models.CharField(
        max_length=3,
        choices=(
            ('inc', 'Include in Email'),
            ('xls', 'XLSX Document'),
            ('txt', 'Text File'),
        ),
        default='inc',
        help_text='Form results are send in this document format',
    )

    content_panels = AbstractEmailForm.content_panels + [
        edit_handlers.MultiFieldPanel([
            edit_handlers.FieldPanel('intro', classname='full'),
            edit_handlers.FieldPanel('thank_you', classname='full'),
        ], 'Page'),
        edit_handlers.MultiFieldPanel([
            edit_handlers.FieldPanel('to_address'),
            edit_handlers.FieldPanel('subject'),
            edit_handlers.FieldPanel('email_content', classname='full'),
            edit_handlers.FieldPanel('attach_as'),
        ], 'Email'),
        edit_handlers.InlinePanel('form_fields', label='Form fields'),
    ]

    def send_mail(self, form):
        kwargs = {
            'title': self.title.replace(' ', '_'),
            'to_addresses': self.to_address.split(','),
            'field_values': self.get_field_values(form),
            'submission_pk': self.get_submission_class().objects.last().pk
        }
        if self.attach_as == 'xls':
            emails.XlsxFormEmail.send(self, **kwargs)
        elif self.attach_as == 'txt':
            emails.TextFormEmail.send(self, **kwargs)
        else:
            emails.FormEmail.send(self, **kwargs)

    def get_field_values(self, form):
        fields = {}
        for field in form:
            value = field.value()
            if isinstance(value, list):
                value = ', '.join(value)
            fields[field.label] = value
        return fields

from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.contrib.settings.models import BaseSiteSetting
from wagtail.contrib.settings.models import register_setting


@register_setting
class HeaderPages(BaseSiteSetting):
    help_page = models.ForeignKey(
        'wagtailcore.Page',
        related_name="help_page",
        verbose_name='Help Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text="Please add a link to the help page.")
    feedback_page = models.ForeignKey(
        'wagtailcore.Page',
        related_name="feedback_page",
        verbose_name='Feedback Form Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text="Please add a link to the feedback form page.")

    panels = [
        FieldPanel('help_page'),
        FieldPanel('feedback_page')
    ]

from django.db import models
from wagtail.admin.panels import PageChooserPanel
from wagtail.contrib.settings.models import BaseSetting
from wagtail.contrib.settings.models import register_setting


@register_setting
class HeaderPages(BaseSetting):
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
        PageChooserPanel('help_page'),
        PageChooserPanel('feedback_page')
    ]

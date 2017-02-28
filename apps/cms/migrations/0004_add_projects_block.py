# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.wagtailcore.fields
import apps.cms.models
import wagtail.wagtailcore.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('meinberlin_cms', '0003_landing_page'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homepage',
            name='body',
            field=wagtail.wagtailcore.fields.StreamField((('paragraph', wagtail.wagtailcore.blocks.RichTextBlock(template='meinberlin_cms/blocks/richtext_block.html')), ('call_to_action', wagtail.wagtailcore.blocks.StructBlock((('body', wagtail.wagtailcore.blocks.RichTextBlock()), ('link', wagtail.wagtailcore.blocks.CharBlock()), ('link_text', wagtail.wagtailcore.blocks.CharBlock(label='Link Text', max_length=50))))), ('columns_text', wagtail.wagtailcore.blocks.StructBlock((('columns_count', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[(2, 'Two columns'), (3, 'Three columns'), (4, 'Four columns')])), ('columns', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.RichTextBlock(label='Column body')))))), ('projects', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock(max_length=80)), ('projects', wagtail.wagtailcore.blocks.ListBlock(apps.cms.models.ProjectSelectionBlock(label='Project')))))))),
        ),
    ]

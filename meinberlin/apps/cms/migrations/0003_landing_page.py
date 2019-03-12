# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.db.models.deletion
import wagtail.core.blocks
import wagtail.core.fields
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0018_remove_rendition_filter'),
        ('meinberlin_cms', '0002_initial_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='header_image',
            field=models.ForeignKey(null=True, to='wagtailimages.Image', on_delete=django.db.models.deletion.SET_NULL, related_name='+'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='subtitle',
            field=models.CharField(default='', max_length=120),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='homepage',
            name='body',
            field=wagtail.core.fields.StreamField((('paragraph', wagtail.core.blocks.RichTextBlock()), ('call_to_action', wagtail.core.blocks.StructBlock((('body', wagtail.core.blocks.RichTextBlock()), ('link', wagtail.core.blocks.CharBlock()), ('link_text', wagtail.core.blocks.CharBlock(label='Link Text', max_length=50))))), ('columns_text', wagtail.core.blocks.StructBlock((('columns_count', wagtail.core.blocks.ChoiceBlock(choices=[(2, 'Two columns'), (3, 'Three columns'), (4, 'Four columns')])), ('columns', wagtail.core.blocks.ListBlock(wagtail.core.blocks.RichTextBlock(label='Column body')))))))),
        ),
    ]

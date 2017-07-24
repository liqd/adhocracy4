# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.wagtailcore.blocks
import wagtail.wagtailcore.fields
import django.db.models.deletion


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
            field=wagtail.wagtailcore.fields.StreamField((('paragraph', wagtail.wagtailcore.blocks.RichTextBlock()), ('call_to_action', wagtail.wagtailcore.blocks.StructBlock((('body', wagtail.wagtailcore.blocks.RichTextBlock()), ('link', wagtail.wagtailcore.blocks.CharBlock()), ('link_text', wagtail.wagtailcore.blocks.CharBlock(label='Link Text', max_length=50))))), ('columns_text', wagtail.wagtailcore.blocks.StructBlock((('columns_count', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[(2, 'Two columns'), (3, 'Three columns'), (4, 'Four columns')])), ('columns', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.RichTextBlock(label='Column body')))))))),
        ),
    ]

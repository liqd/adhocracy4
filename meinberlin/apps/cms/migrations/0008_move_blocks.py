# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import wagtail.blocks
import wagtail.fields
from django.db import migrations
from django.db import models

import meinberlin.apps.cms.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('meinberlin_cms', '0007_simplepage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homepage',
            name='body',
            field=wagtail.fields.StreamField((('paragraph', wagtail.blocks.RichTextBlock(template='meinberlin_cms/blocks/richtext_block.html')), ('call_to_action', wagtail.blocks.StructBlock((('body', wagtail.blocks.RichTextBlock()), ('link', wagtail.blocks.CharBlock()), ('link_text', wagtail.blocks.CharBlock(max_length=50, label='Link Text'))))), ('columns_text', wagtail.blocks.StructBlock((('columns_count', wagtail.blocks.ChoiceBlock(choices=[(2, 'Two columns'), (3, 'Three columns'), (4, 'Four columns')])), ('columns', wagtail.blocks.ListBlock(wagtail.blocks.RichTextBlock(label='Column body')))))), ('projects', wagtail.blocks.StructBlock((('title', wagtail.blocks.CharBlock(max_length=80)), ('projects', wagtail.blocks.ListBlock(meinberlin.apps.cms.blocks.ProjectSelectionBlock(label='Project')))))), ('activities', wagtail.blocks.StructBlock((('heading', wagtail.blocks.CharBlock(label='Heading')), ('count', wagtail.blocks.IntegerBlock(default=5, label='Count'))))))),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import meinberlin.apps.cms.blocks
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('meinberlin_cms', '0007_simplepage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homepage',
            name='body',
            field=wagtail.core.fields.StreamField((('paragraph', wagtail.core.blocks.RichTextBlock(template='meinberlin_cms/blocks/richtext_block.html')), ('call_to_action', wagtail.core.blocks.StructBlock((('body', wagtail.core.blocks.RichTextBlock()), ('link', wagtail.core.blocks.CharBlock()), ('link_text', wagtail.core.blocks.CharBlock(max_length=50, label='Link Text'))))), ('columns_text', wagtail.core.blocks.StructBlock((('columns_count', wagtail.core.blocks.ChoiceBlock(choices=[(2, 'Two columns'), (3, 'Three columns'), (4, 'Four columns')])), ('columns', wagtail.core.blocks.ListBlock(wagtail.core.blocks.RichTextBlock(label='Column body')))))), ('projects', wagtail.core.blocks.StructBlock((('title', wagtail.core.blocks.CharBlock(max_length=80)), ('projects', wagtail.core.blocks.ListBlock(meinberlin.apps.cms.blocks.ProjectSelectionBlock(label='Project')))))), ('activities', wagtail.core.blocks.StructBlock((('heading', wagtail.core.blocks.CharBlock(label='Heading')), ('count', wagtail.core.blocks.IntegerBlock(default=5, label='Count'))))))),
        ),
    ]

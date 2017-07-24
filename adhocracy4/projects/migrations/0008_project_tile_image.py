# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import adhocracy4.images.fields


class Migration(migrations.Migration):

    dependencies = [
        ('a4projects', '0007_add_verbose_names'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='tile_image',
            field=adhocracy4.images.fields.ConfiguredImageField('tileimage', verbose_name='Tile image', blank=True, upload_to='projects/tiles', help_prefix='The image will be shown in the project tile.'),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import adhocracy4.images.fields


class Migration(migrations.Migration):

    dependencies = [
        ('a4projects', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='image',
            field=adhocracy4.images.fields.ConfiguredImageField('heroimage', help_prefix='The image will be shown as a decorative background image.', upload_to='projects/backgrounds', verbose_name='Header image', blank=True),
        ),
    ]

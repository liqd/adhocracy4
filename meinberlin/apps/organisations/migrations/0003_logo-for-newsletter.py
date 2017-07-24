# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import adhocracy4.images.fields


class Migration(migrations.Migration):

    dependencies = [
        ('meinberlin_organisations', '0002_auto_20170130_0859'),
    ]

    operations = [
        migrations.AddField(
            model_name='organisation',
            name='logo',
            field=adhocracy4.images.fields.ConfiguredImageField('logo', verbose_name='Logo', help_prefix='The image will be shown in the newsletter in the banner.', upload_to='organisations/logo', blank=True),
        ),
    ]

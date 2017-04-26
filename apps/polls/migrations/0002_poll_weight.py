# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meinberlin_polls', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='poll',
            name='weight',
            field=models.SmallIntegerField(default=0),
            preserve_default=False,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a4projects', '0005_auto_20170313_1407'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='typ',
            field=models.CharField(verbose_name='Type of the project', max_length=120, blank=True),
        ),
    ]

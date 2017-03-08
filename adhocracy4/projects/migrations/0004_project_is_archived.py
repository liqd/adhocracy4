# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a4projects', '0003_auto_20170130_0836'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='is_archived',
            field=models.BooleanField(verbose_name='Project is archived', default=False, help_text='Enable to archive the project'),
        ),
    ]

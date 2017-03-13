# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a4projects', '0004_project_is_archived'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ['-created']},
        ),
        migrations.AlterField(
            model_name='project',
            name='is_archived',
            field=models.BooleanField(verbose_name='Project is archived', default=False, help_text='Set to archive the project'),
        ),
    ]

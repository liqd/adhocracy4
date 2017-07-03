# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a4actions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='action',
            name='verb',
            field=models.CharField(max_length=255, choices=[('create', 'CREATE'), ('add', 'ADD'), ('update', 'UPDATE'), ('complete', 'COMPLETE'), ('schedule', 'SCHEDULE'), ('start', 'START')], db_index=True),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('meinberlin_budgeting', '0002_proposal_point_label'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proposal',
            name='category',
            field=models.ForeignKey(blank=True, related_name='+', on_delete=django.db.models.deletion.SET_NULL, null=True, to='a4categories.Category'),
        ),
    ]

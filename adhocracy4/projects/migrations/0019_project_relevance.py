# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-11-12 12:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a4projects', '0018_add_location_and_topic'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='relevance',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=4),
        ),
    ]

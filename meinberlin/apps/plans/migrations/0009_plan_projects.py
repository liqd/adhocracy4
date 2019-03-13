# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-04-16 15:10
from __future__ import unicode_literals

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ('a4projects', '0014_collapsible_information_field'),
        ('meinberlin_plans', '0008_add_some_verbose_names'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='projects',
            field=models.ManyToManyField(blank=True, related_name='plans', to='a4projects.Project'),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-04-11 11:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meinberlin_ideas', '0013_idea_labels'),
    ]

    operations = [
        migrations.AlterField(
            model_name='idea',
            name='labels',
            field=models.ManyToManyField(related_name='meinberlin_ideas_idea_label', to='a4labels.Label', verbose_name='Labels'),
        ),
    ]

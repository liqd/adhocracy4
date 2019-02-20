# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-02-08 13:04
from __future__ import unicode_literals

import adhocracy4.maps.fields
import adhocracy4.projects.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('a4projects', '0020_update_verbose_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='point',
            field=adhocracy4.maps.fields.PointField(blank=True, help_text='Locate your project. Click inside the marked area or type in an address to set the marker. A set marker can be dragged when pressed.', null=True, verbose_name='Can your project be located on the map?'),
        ),
        migrations.AlterField(
            model_name='project',
            name='topics',
            field=adhocracy4.projects.fields.TopicField(default='', help_text='Add topics to your project.', max_length=254, verbose_name='Project topics'),
        ),
    ]

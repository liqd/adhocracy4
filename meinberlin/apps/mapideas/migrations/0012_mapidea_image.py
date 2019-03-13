# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-21 08:10
from __future__ import unicode_literals

from django.db import migrations

import adhocracy4.images.fields


class Migration(migrations.Migration):

    dependencies = [
        ('meinberlin_mapideas', '0011_moderateable'),
    ]

    operations = [
        migrations.AddField(
            model_name='mapidea',
            name='image',
            field=adhocracy4.images.fields.ConfiguredImageField('idea_image', blank=True, upload_to='ideas/images'),
        ),
    ]

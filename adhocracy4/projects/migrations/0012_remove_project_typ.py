# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-21 15:18
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("a4projects", "0011_fix_copyright_field_desc"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="project",
            name="typ",
        ),
    ]

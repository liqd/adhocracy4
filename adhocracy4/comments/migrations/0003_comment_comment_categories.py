# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-07-17 13:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("a4comments", "0002_extend_comments_field"),
    ]

    operations = [
        migrations.AddField(
            model_name="comment",
            name="comment_categories",
            field=models.CharField(blank=True, max_length=256),
        ),
    ]

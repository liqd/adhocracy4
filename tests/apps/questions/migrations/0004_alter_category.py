# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-28 09:28
from __future__ import unicode_literals

import adhocracy4.categories.fields
from django.db import migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("a4test_questions", "0003_remove_related_set"),
    ]

    operations = [
        migrations.AlterField(
            model_name="question",
            name="category",
            field=adhocracy4.categories.fields.CategoryField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="a4categories.Category",
            ),
        ),
    ]

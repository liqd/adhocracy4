# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("a4categories", "__first__"),
        ("meinberlin_ideas", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="idea",
            name="category",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="a4categories.Category",
            ),
        ),
    ]

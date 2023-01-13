# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("meinberlin_ideas", "0003_auto_20170309_1006"),
    ]

    operations = [
        migrations.AlterField(
            model_name="idea",
            name="category",
            field=models.ForeignKey(
                blank=True,
                related_name="+",
                on_delete=django.db.models.deletion.SET_NULL,
                null=True,
                to="a4categories.Category",
            ),
        ),
    ]

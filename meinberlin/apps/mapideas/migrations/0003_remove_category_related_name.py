# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("meinberlin_mapideas", "0002_mapidea_point_label"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mapidea",
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

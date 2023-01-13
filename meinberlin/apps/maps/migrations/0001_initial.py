# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations
from django.db import models

import adhocracy4.maps.fields


class Migration(migrations.Migration):

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="MapPreset",
            fields=[
                (
                    "id",
                    models.AutoField(
                        serialize=False,
                        primary_key=True,
                        auto_created=True,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=128)),
                ("polygon", adhocracy4.maps.fields.MultiPolygonField()),
            ],
        ),
        migrations.CreateModel(
            name="MapPresetCategory",
            fields=[
                (
                    "id",
                    models.AutoField(
                        serialize=False,
                        primary_key=True,
                        auto_created=True,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=128)),
            ],
        ),
        migrations.AddField(
            model_name="mappreset",
            name="category",
            field=models.ForeignKey(
                blank=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="meinberlin_maps.MapPresetCategory",
                null=True,
            ),
        ),
    ]

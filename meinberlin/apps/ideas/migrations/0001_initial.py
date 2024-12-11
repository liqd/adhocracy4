# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import autoslug.fields
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("a4modules", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Idea",
            fields=[
                (
                    "item_ptr",
                    models.OneToOneField(
                        primary_key=True,
                        parent_link=True,
                        to="a4modules.Item",
                        auto_created=True,
                        serialize=False,
                        on_delete=models.CASCADE,
                    ),
                ),
                (
                    "slug",
                    autoslug.fields.AutoSlugField(
                        unique=True, populate_from="name", editable=False
                    ),
                ),
                ("name", models.CharField(max_length=120)),
                ("description", models.TextField()),
            ],
            options={
                "abstract": False,
            },
            bases=("a4modules.item",),
        ),
    ]

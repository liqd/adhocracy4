# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import autoslug.fields
from django.conf import settings
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Organisation",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        primary_key=True,
                        serialize=False,
                        auto_created=True,
                    ),
                ),
                (
                    "slug",
                    autoslug.fields.AutoSlugField(
                        unique=True, editable=False, populate_from="name"
                    ),
                ),
                ("name", models.CharField(max_length=512)),
                ("initiators", models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("a4projects", "0006_project_typ"),
    ]

    operations = [
        migrations.CreateModel(
            name="ExternalProject",
            fields=[
                (
                    "project_ptr",
                    models.OneToOneField(
                        parent_link=True,
                        auto_created=True,
                        to="a4projects.Project",
                        serialize=False,
                        primary_key=True,
                        on_delete=models.CASCADE,
                    ),
                ),
                ("url", models.URLField()),
            ],
            options={
                "abstract": False,
            },
            bases=("a4projects.project",),
        ),
    ]

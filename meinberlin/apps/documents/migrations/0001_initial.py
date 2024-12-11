# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.utils.timezone
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("a4modules", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Document",
            fields=[
                (
                    "item_ptr",
                    models.OneToOneField(
                        primary_key=True,
                        serialize=False,
                        auto_created=True,
                        parent_link=True,
                        to="a4modules.Item",
                        on_delete=models.CASCADE,
                    ),
                ),
                ("name", models.CharField(max_length=120)),
            ],
            options={
                "abstract": False,
            },
            bases=("a4modules.item",),
        ),
        migrations.CreateModel(
            name="Paragraph",
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
                    "created",
                    models.DateTimeField(
                        default=django.utils.timezone.now, editable=False
                    ),
                ),
                (
                    "modified",
                    models.DateTimeField(blank=True, null=True, editable=False),
                ),
                ("name", models.CharField(max_length=120, blank=True)),
                ("text", models.TextField()),
                ("weight", models.PositiveIntegerField()),
                (
                    "document",
                    models.ForeignKey(
                        related_name="paragraphs",
                        to="meinberlin_documents.Document",
                        on_delete=models.CASCADE,
                    ),
                ),
            ],
            options={
                "ordering": ("weight",),
            },
        ),
    ]

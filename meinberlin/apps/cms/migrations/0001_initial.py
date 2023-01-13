# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import modelcluster.fields
import wagtail.fields
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("wagtailcore", "0030_index_on_pagerevision_created_at"),
    ]

    operations = [
        migrations.CreateModel(
            name="HomePage",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        to="wagtailcore.Page",
                        serialize=False,
                        auto_created=True,
                        parent_link=True,
                        primary_key=True,
                        on_delete=models.CASCADE,
                    ),
                ),
                ("body", wagtail.fields.RichTextField(blank=True)),
            ],
            options={
                "abstract": False,
            },
            bases=("wagtailcore.page",),
        ),
        migrations.CreateModel(
            name="MenuItem",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        auto_created=True,
                        serialize=False,
                        primary_key=True,
                    ),
                ),
                ("title", models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="NavigationMenu",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        auto_created=True,
                        serialize=False,
                        primary_key=True,
                    ),
                ),
                ("title", models.CharField(max_length=255)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="NavigationMenuItem",
            fields=[
                (
                    "menuitem_ptr",
                    models.OneToOneField(
                        to="meinberlin_cms.MenuItem",
                        serialize=False,
                        auto_created=True,
                        parent_link=True,
                        primary_key=True,
                        on_delete=models.CASCADE,
                    ),
                ),
                (
                    "sort_order",
                    models.IntegerField(blank=True, null=True, editable=False),
                ),
                (
                    "parent",
                    modelcluster.fields.ParentalKey(
                        related_name="items", to="meinberlin_cms.NavigationMenu"
                    ),
                ),
            ],
            options={
                "abstract": False,
                "ordering": ["sort_order"],
            },
            bases=("meinberlin_cms.menuitem", models.Model),
        ),
        migrations.AddField(
            model_name="menuitem",
            name="link_page",
            field=models.ForeignKey(to="wagtailcore.Page", on_delete=models.CASCADE),
        ),
    ]

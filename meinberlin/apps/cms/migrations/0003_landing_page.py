# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.db.models.deletion
import wagtail.blocks
import wagtail.fields
from django.db import migrations
from django.db import models


def empty_to_valid_json(apps, schema_editor):
    HomePage = apps.get_model("meinberlin_cms", "HomePage")

    q_homepage = HomePage.objects.all()
    if q_homepage:
        for homepage in q_homepage:
            if len(homepage.body) == 0:
                homepage.body = "{}"
                homepage.save()


class Migration(migrations.Migration):
    dependencies = [
        ("wagtailimages", "0018_remove_rendition_filter"),
        ("meinberlin_cms", "0002_initial_data"),
    ]

    operations = [
        migrations.RunPython(empty_to_valid_json),
        migrations.AddField(
            model_name="homepage",
            name="header_image",
            field=models.ForeignKey(
                null=True,
                to="wagtailimages.Image",
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
            ),
        ),
        migrations.AddField(
            model_name="homepage",
            name="subtitle",
            field=models.CharField(default="", max_length=120),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="homepage",
            name="body",
            field=wagtail.fields.StreamField(
                (
                    ("paragraph", wagtail.blocks.RichTextBlock()),
                    (
                        "call_to_action",
                        wagtail.blocks.StructBlock(
                            (
                                ("body", wagtail.blocks.RichTextBlock()),
                                ("link", wagtail.blocks.CharBlock()),
                                (
                                    "link_text",
                                    wagtail.blocks.CharBlock(
                                        label="Link Text", max_length=50
                                    ),
                                ),
                            )
                        ),
                    ),
                    (
                        "columns_text",
                        wagtail.blocks.StructBlock(
                            (
                                (
                                    "columns_count",
                                    wagtail.blocks.ChoiceBlock(
                                        choices=[
                                            (2, "Two columns"),
                                            (3, "Three columns"),
                                            (4, "Four columns"),
                                        ]
                                    ),
                                ),
                                (
                                    "columns",
                                    wagtail.blocks.ListBlock(
                                        wagtail.blocks.RichTextBlock(
                                            label="Column body"
                                        )
                                    ),
                                ),
                            )
                        ),
                    ),
                )
            ),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.utils.timezone
from django.conf import settings
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("meinberlin_budgeting", "0002_proposal_moderator_feedback"),
    ]

    operations = [
        migrations.CreateModel(
            name="ModeratorStatement",
            fields=[
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
                (
                    "proposal",
                    models.OneToOneField(
                        related_name="moderator_statement",
                        primary_key=True,
                        serialize=False,
                        to="meinberlin_budgeting.Proposal",
                        on_delete=models.CASCADE,
                    ),
                ),
                ("statement", models.TextField(blank=True)),
                (
                    "creator",
                    models.ForeignKey(
                        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]

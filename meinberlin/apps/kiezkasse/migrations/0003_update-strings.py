# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("meinberlin_kiezkasse", "0002_add_moderator_feedback"),
    ]

    operations = [
        migrations.AlterField(
            model_name="proposal",
            name="creator_contribution",
            field=models.BooleanField(
                default=False,
                help_text="I want to contribute to the proposal myself.",
                verbose_name="Own contribution to the proposal",
            ),
        ),
    ]

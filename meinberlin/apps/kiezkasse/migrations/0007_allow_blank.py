# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("meinberlin_kiezkasse", "0006_add_default_ordering"),
    ]

    operations = [
        migrations.AlterField(
            model_name="proposal",
            name="moderator_statement",
            field=models.OneToOneField(
                null=True,
                related_name="+",
                to="meinberlin_moderatorfeedback.ModeratorStatement",
                blank=True,
                on_delete=models.CASCADE,
            ),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("meinberlin_newsletters", "0004_add_initiator_option"),
    ]

    operations = [
        migrations.AlterField(
            model_name="newsletter",
            name="receivers",
            field=models.PositiveSmallIntegerField(
                choices=[
                    (2, "Users following a specific project"),
                    (1, "Users following your organisation"),
                    (3, "Every initiator of your organisation"),
                    (0, "Every user of the platform"),
                ],
                verbose_name="Receivers",
            ),
        ),
    ]

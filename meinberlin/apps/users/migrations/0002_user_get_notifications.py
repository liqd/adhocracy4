# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("meinberlin_users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="get_notifications",
            field=models.BooleanField(
                verbose_name="Send me email notifications",
                default=True,
                help_text="Designates whether you want to receive notifications. Unselect if you do not want to receive notifications.",
            ),
        ),
    ]

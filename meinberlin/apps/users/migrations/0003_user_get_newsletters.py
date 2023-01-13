# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("meinberlin_users", "0002_user_get_notifications"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="get_newsletters",
            field=models.BooleanField(
                help_text="Designates whether you want to receive newsletters. Unselect if you do not want to receive newsletters.",
                default=True,
                verbose_name="Send me newsletters",
            ),
        ),
    ]

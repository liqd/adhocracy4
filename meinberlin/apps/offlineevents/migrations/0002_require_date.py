# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("meinberlin_offlineevents", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="offlineevent",
            name="date",
            field=models.DateTimeField(
                verbose_name="Date", default=datetime.datetime(1970, 1, 1, 1, 0)
            ),
            preserve_default=False,
        ),
    ]

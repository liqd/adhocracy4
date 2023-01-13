# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("meinberlin_kiezkasse", "0005_auto_20170529_1302"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="proposal",
            options={"ordering": ["-created"]},
        ),
    ]

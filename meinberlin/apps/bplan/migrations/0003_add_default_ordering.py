# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("meinberlin_bplan", "0002_auto_20170509_1358"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="statement",
            options={"ordering": ["-created"]},
        ),
    ]

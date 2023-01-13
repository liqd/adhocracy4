# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("meinberlin_maps", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="mappreset",
            options={"ordering": ["name"]},
        ),
    ]

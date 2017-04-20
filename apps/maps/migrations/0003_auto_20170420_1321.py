# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meinberlin_maps', '0002_auto_20170420_1313'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mappresetcategory',
            options={'ordering': ['name']},
        ),
    ]

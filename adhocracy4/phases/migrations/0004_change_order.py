# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a4phases', '0003_fill_weight_field'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='phase',
            options={'ordering': ['weight']},
        ),
    ]

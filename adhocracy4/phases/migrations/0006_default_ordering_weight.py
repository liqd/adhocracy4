# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a4phases', '0005_add_verbose_names'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='phase',
            options={'ordering': ['module__weight', 'weight']},
        ),
    ]

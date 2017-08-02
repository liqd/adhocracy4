# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meinberlin_newsletters', '0002_add-sender-name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsletter',
            name='receivers',
            field=models.PositiveSmallIntegerField(default='', verbose_name='Receivers', choices=[(0, 'Every user on the platform'), (1, 'Users following the chosen organisation'), (2, 'Users following the chosen project')]),
        ),
    ]

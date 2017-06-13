# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a4actions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
            ],
            options={
                'ordering': ('-timestamp',),
                'proxy': True,
            },
            bases=('a4actions.action',),
        ),
    ]

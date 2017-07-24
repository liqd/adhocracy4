# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meinberlin_newsletters', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsletter',
            name='sender_name',
            field=models.CharField(verbose_name='Name', max_length=254, default=''),
            preserve_default=False,
        ),
    ]

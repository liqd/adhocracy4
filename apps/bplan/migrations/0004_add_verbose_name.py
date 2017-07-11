# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meinberlin_bplan', '0003_add_default_ordering'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bplan',
            name='office_worker_email',
            field=models.EmailField(verbose_name='Office worker email', max_length=254),
        ),
    ]

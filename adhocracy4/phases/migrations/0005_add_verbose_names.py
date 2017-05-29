# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a4phases', '0004_change_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phase',
            name='description',
            field=models.TextField(verbose_name='Description', max_length=300),
        ),
        migrations.AlterField(
            model_name='phase',
            name='end_date',
            field=models.DateTimeField(verbose_name='End date', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='phase',
            name='name',
            field=models.CharField(verbose_name='Name', max_length=80),
        ),
        migrations.AlterField(
            model_name='phase',
            name='start_date',
            field=models.DateTimeField(verbose_name='Start date', null=True, blank=True),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meinberlin_bplan', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statement',
            name='email',
            field=models.EmailField(verbose_name='Email address', max_length=254, blank=True),
        ),
        migrations.AlterField(
            model_name='statement',
            name='name',
            field=models.CharField(verbose_name='Your Name', max_length=255),
        ),
        migrations.AlterField(
            model_name='statement',
            name='postal_code_city',
            field=models.CharField(verbose_name='Postal code, City', max_length=255),
        ),
        migrations.AlterField(
            model_name='statement',
            name='statement',
            field=models.TextField(verbose_name='Statement', max_length=17500),
        ),
        migrations.AlterField(
            model_name='statement',
            name='street_number',
            field=models.CharField(verbose_name='Street, House number', max_length=255),
        ),
    ]

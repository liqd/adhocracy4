# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a4modules', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=120)),
                ('module', models.ForeignKey(to='a4modules.Module', on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name_plural': 'categories',
            },
        ),
    ]

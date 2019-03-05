# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import adhocracy4.maps.fields


class Migration(migrations.Migration):

    dependencies = [
        ('a4modules', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AreaSettings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('polygon', adhocracy4.maps.fields.MultiPolygonField()),
                ('module', models.OneToOneField(related_name='areasettings_settings', to='a4modules.Module', on_delete=models.CASCADE)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

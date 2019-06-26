# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import autoslug.fields
import adhocracy4.maps.fields


class Migration(migrations.Migration):

    dependencies = [
        ('a4modules', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('item_ptr', models.OneToOneField(primary_key=True, serialize=False, auto_created=True, parent_link=True, to='a4modules.Item', on_delete=models.CASCADE)),
                ('slug', autoslug.fields.AutoSlugField(unique=True, editable=False, populate_from='name')),
                ('name', models.CharField(max_length=120)),
                ('point', adhocracy4.maps.fields.PointField()),
            ],
            options={
                'abstract': False,
            },
            bases=('a4modules.item',),
        ),
    ]

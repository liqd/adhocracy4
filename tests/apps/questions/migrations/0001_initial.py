# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a4modules', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('item_ptr', models.OneToOneField(serialize=False, primary_key=True, to='a4modules.Item', auto_created=True, parent_link=True, on_delete=models.CASCADE)),
                ('text', models.CharField(max_length=120, default='Can i haz cheezburger, pls?')),
            ],
            options={
                'abstract': False,
            },
            bases=('a4modules.item',),
        ),
    ]

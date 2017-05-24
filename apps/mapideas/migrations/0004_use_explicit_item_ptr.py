# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meinberlin_mapideas', '0003_remove_category_related_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mapidea',
            name='item_ptr',
            field=models.OneToOneField(to='a4modules.Item', serialize=False, primary_key=True, related_name='meinberlin_mapideas_mapidea', parent_link=True),
        ),
    ]

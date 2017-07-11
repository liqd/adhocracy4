# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import adhocracy4.maps.fields


class Migration(migrations.Migration):

    dependencies = [
        ('a4maps', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='areasettings',
            name='polygon',
            field=adhocracy4.maps.fields.MultiPolygonField(help_text='Please draw an area on the map.', verbose_name='Polygon'),
        ),
    ]

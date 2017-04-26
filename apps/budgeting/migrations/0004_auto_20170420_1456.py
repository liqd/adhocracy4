# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import adhocracy4.maps.fields


class Migration(migrations.Migration):

    dependencies = [
        ('meinberlin_budgeting', '0003_moderatorstatement'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='proposal',
            options={},
        ),
        migrations.AddField(
            model_name='proposal',
            name='point',
            field=adhocracy4.maps.fields.PointField(default=None, verbose_name='Where can your idea be located on a map?', help_text='Click inside marked area to set a marker. Drag and drop marker to change place.'),
            preserve_default=False,
        ),
    ]

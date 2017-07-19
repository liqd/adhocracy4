# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meinberlin_mapideas', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mapidea',
            name='point_label',
            field=models.CharField(max_length=255, verbose_name='Label of the ideas location', help_text='The label of the ideas location. This could be an address or the name of a landmark.', blank=True, default=''),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meinberlin_polls', '0002_poll_weight'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choice',
            name='poll',
            field=models.ForeignKey(related_name='choices', to='meinberlin_polls.Poll'),
        ),
        migrations.AlterField(
            model_name='vote',
            name='choice',
            field=models.ForeignKey(related_name='votes', to='meinberlin_polls.Choice'),
        ),
    ]

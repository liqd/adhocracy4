# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('euth_reports', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='report',
            old_name='user',
            new_name='creator',
        ),
    ]

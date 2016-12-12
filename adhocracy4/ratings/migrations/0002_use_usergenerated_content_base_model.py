# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a4ratings', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rating',
            old_name='user',
            new_name='creator',
        ),
        migrations.AlterUniqueTogether(
            name='rating',
            unique_together=set([('content_type', 'object_pk', 'creator')]),
        ),
    ]

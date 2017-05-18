# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meinberlin_budgeting', '0003_remove_category_related_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='moderatorstatement',
            name='creator',
        ),
        migrations.RemoveField(
            model_name='moderatorstatement',
            name='proposal',
        ),
        migrations.RemoveField(
            model_name='proposal',
            name='moderator_feedback',
        ),
        migrations.DeleteModel(
            name='ModeratorStatement',
        ),
    ]

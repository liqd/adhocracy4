# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import meinberlin.apps.moderatorfeedback.fields


class Migration(migrations.Migration):

    dependencies = [
        ('meinberlin_budgeting', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposal',
            name='moderator_feedback',
            field=meinberlin.apps.moderatorfeedback.fields.ModeratorFeedbackField(choices=[('CONSIDERATION', 'Under consideration'), ('REJECTED', 'Rejected'), ('ACCEPTED', 'Accepted')]),
        ),
    ]

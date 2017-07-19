# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import apps.moderatorfeedback.fields


class Migration(migrations.Migration):

    dependencies = [
        ('meinberlin_moderatorfeedback', '__first__'),
        ('meinberlin_kiezkasse', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposal',
            name='moderator_feedback',
            field=apps.moderatorfeedback.fields.ModeratorFeedbackField(null=True, choices=[('CONSIDERATION', 'Under consideration'), ('REJECTED', 'Rejected'), ('ACCEPTED', 'Accepted')], default=None, max_length=254, blank=True),
        ),
        migrations.AddField(
            model_name='proposal',
            name='moderator_statement',
            field=models.OneToOneField(null=True, related_name='+', to='meinberlin_moderatorfeedback.ModeratorStatement'),
        ),
    ]

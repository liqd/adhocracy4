# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations

from adhocracy4.phases.models import Phase


def _remove_feedback_phase(apps, schema_editor):
    Phase.objects.filter(
        type='meinberlin_budgeting:040:feedback'
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('meinberlin_budgeting', '0008_auto_20170529_1302'),
    ]

    operations = [
        migrations.RunPython(_remove_feedback_phase)
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

def set_weight(apps, schema_editor):
    Phase = apps.get_model('a4phases', 'Phase')
    for phase in Phase.objects.all():
        weight = int(phase.type.split(':')[1])
        phase.weight = weight
        phase.save()


class Migration(migrations.Migration):

    dependencies = [
        ('a4phases', '0002_phase_weight'),
    ]

    operations = [
        migrations.RunPython(set_weight)
    ]

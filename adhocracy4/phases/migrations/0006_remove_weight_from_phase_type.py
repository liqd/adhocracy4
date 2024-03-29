# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-12-20 12:42
from __future__ import unicode_literals

from django.db import migrations


def remove_weight_from_type_string(apps, schema_editor):
    Phase = apps.get_model("a4phases", "Phase")
    for phase in Phase.objects.all():
        parts = phase.type.split(":")
        phase.type = ":".join([parts[0], parts[2]])
        phase.save()


def add_weight_from_type_string(apps, schema_editor):
    Phase = apps.get_model("a4phases", "Phase")
    for phase in Phase.objects.all():
        parts = phase.type.split(":")
        phase.type = ":".join([parts[0], str(phase.weight), parts[1]])
        phase.save()


class Migration(migrations.Migration):

    dependencies = [
        ("a4phases", "0005_add_verbose_names"),
    ]

    operations = [
        migrations.RunPython(
            remove_weight_from_type_string, add_weight_from_type_string
        )
    ]

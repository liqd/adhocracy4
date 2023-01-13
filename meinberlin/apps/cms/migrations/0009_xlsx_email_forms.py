# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("meinberlin_cms", "0008_move_blocks"),
    ]

    operations = [
        migrations.AlterField(
            model_name="emailformpage",
            name="attach_as",
            field=models.CharField(
                max_length=3,
                default="xlsx",
                choices=[("xlsx", "XLSX Document"), ("txt", "Text")],
                help_text="Form results are send in this document format",
            ),
        ),
    ]

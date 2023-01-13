# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("meinberlin_cms", "0009_xlsx_email_forms"),
    ]

    operations = [
        migrations.AlterField(
            model_name="emailformpage",
            name="attach_as",
            field=models.CharField(
                max_length=3,
                default="xls",
                choices=[("xls", "XLSX Document"), ("txt", "Text")],
                help_text="Form results are send in this document format",
            ),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ("meinberlin_documents", "0001_initial"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Document",
            new_name="Chapter",
        ),
        migrations.RenameField(
            model_name="paragraph",
            old_name="document",
            new_name="chapter",
        ),
    ]

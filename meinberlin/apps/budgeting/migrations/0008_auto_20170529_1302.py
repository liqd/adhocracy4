# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import ckeditor.fields
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ('meinberlin_budgeting', '0007_update-strings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proposal',
            name='description',
            field=ckeditor.fields.RichTextField(verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='name',
            field=models.CharField(max_length=120, verbose_name='Name'),
        ),
    ]

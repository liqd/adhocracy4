# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import ckeditor_uploader.fields


class Migration(migrations.Migration):

    dependencies = [
        ('a4projects', '0006_project_typ'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='result',
            field=ckeditor_uploader.fields.RichTextUploadingField(verbose_name='Results of your project', blank=True, help_text='Here you should explain what the expected outcome of the project will be and how you are planning to use the results. If the project is finished you should add a summary of the results.'),
        ),
    ]

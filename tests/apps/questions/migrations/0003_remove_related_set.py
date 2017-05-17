# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('a4test_questions', '0002_question_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='category',
            field=models.ForeignKey(blank=True, to='a4categories.Category', related_name='+', on_delete=django.db.models.deletion.SET_NULL, null=True),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import adhocracy4.phases.validators


class Migration(migrations.Migration):

    dependencies = [
        ('a4modules', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Phase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=80)),
                ('description', models.TextField(max_length=300)),
                ('type', models.CharField(validators=[adhocracy4.phases.validators.validate_content], max_length=128)),
                ('start_date', models.DateTimeField(null=True, blank=True)),
                ('end_date', models.DateTimeField(null=True, blank=True)),
                ('module', models.ForeignKey(to='a4modules.Module', on_delete=models.CASCADE)),
            ],
            options={
                'ordering': ['type'],
            },
        ),
    ]

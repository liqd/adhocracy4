# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('a4modules', '0001_initial'),
        ('meinberlin_extprojects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bplan',
            fields=[
                ('externalproject_ptr', models.OneToOneField(parent_link=True, serialize=False, auto_created=True, to='meinberlin_extprojects.ExternalProject', primary_key=True)),
                ('office_worker_email', models.EmailField(max_length=254)),
            ],
            options={
                'abstract': False,
            },
            bases=('meinberlin_extprojects.externalproject',),
        ),
        migrations.CreateModel(
            name='Statement',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('created', models.DateTimeField(editable=False, default=django.utils.timezone.now)),
                ('modified', models.DateTimeField(editable=False, blank=True, null=True)),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('statement', models.TextField(max_length=17500)),
                ('street_number', models.CharField(max_length=255)),
                ('postal_code_city', models.CharField(max_length=255)),
                ('module', models.ForeignKey(to='a4modules.Module')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import autoslug.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('a4projects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(editable=False, default=django.utils.timezone.now)),
                ('modified', models.DateTimeField(blank=True, editable=False, null=True)),
                ('creator', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=512, unique=True)),
                ('slug', autoslug.fields.AutoSlugField(populate_from='name', editable=False, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('weight', models.PositiveIntegerField()),
                ('project', models.ForeignKey(to='a4projects.Project', on_delete=models.CASCADE)),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='module',
            field=models.ForeignKey(to='a4modules.Module', on_delete=models.CASCADE),
        ),
    ]

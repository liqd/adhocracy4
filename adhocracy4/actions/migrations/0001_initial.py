# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('a4projects', '0006_project_typ'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('target_object_id', models.CharField(max_length=255, blank=True, null=True)),
                ('obj_object_id', models.CharField(max_length=255, blank=True, null=True)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('public', models.BooleanField(db_index=True, default=True)),
                ('verb', models.CharField(max_length=255, db_index=True, choices=[('create', 'CREATE'), ('add', 'ADD'), ('update', 'UPDATE'), ('complete', 'COMPLETE'), ('schedule', 'SCHEDULE')])),
                ('description', models.TextField(blank=True, null=True)),
                ('actor', models.ForeignKey(blank=True, null=True, to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
                ('obj_content_type', models.ForeignKey(blank=True, null=True, related_name='obj', to='contenttypes.ContentType', on_delete=models.CASCADE)),
                ('project', models.ForeignKey(blank=True, null=True, to='a4projects.Project', on_delete=models.CASCADE)),
                ('target_content_type', models.ForeignKey(blank=True, null=True, related_name='target', to='contenttypes.ContentType', on_delete=models.CASCADE)),
            ],
        ),
    ]

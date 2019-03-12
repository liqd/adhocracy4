# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('a4projects', '0006_project_typ'),
    ]

    operations = [
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('modified', models.DateTimeField(null=True, blank=True, editable=False)),
                ('enabled', models.BooleanField(default=True)),
                ('creator', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
                ('project', models.ForeignKey(to='a4projects.Project', on_delete=models.CASCADE)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='follow',
            unique_together=set([('project', 'creator')]),
        ),
    ]

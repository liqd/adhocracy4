# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.utils.timezone
import ckeditor_uploader.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.A4_ORGANISATIONS_MODEL),
        ('a4projects', '0008_project_tile_image'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Newsletter',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('created', models.DateTimeField(editable=False, default=django.utils.timezone.now)),
                ('modified', models.DateTimeField(null=True, editable=False, blank=True)),
                ('sender', models.EmailField(max_length=254, blank=True, verbose_name='Sender')),
                ('subject', models.CharField(max_length=254, verbose_name='Subject')),
                ('body', ckeditor_uploader.fields.RichTextUploadingField(blank=True, verbose_name='Email body')),
                ('sent', models.DateTimeField(null=True, blank=True, verbose_name='Sent')),
                ('receivers', models.PositiveSmallIntegerField(choices=[(0, 'Every user on the platform'), (1, 'Users following the chosen organisation'), (2, 'Users following the chosen project')], verbose_name='Receivers')),
                ('creator', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('organisation', models.ForeignKey(null=True, to=settings.A4_ORGANISATIONS_MODEL, blank=True)),
                ('project', models.ForeignKey(null=True, to='a4projects.Project', blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

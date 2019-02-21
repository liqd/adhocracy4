# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import ckeditor_uploader.fields
import django.utils.timezone
from django.conf import settings
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        migrations.swappable_dependency(settings.A4_ORGANISATIONS_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('created', models.DateTimeField(editable=False, default=django.utils.timezone.now)),
                ('modified', models.DateTimeField(null=True, editable=False, blank=True)),
                ('slug', autoslug.fields.AutoSlugField(unique=True, editable=False, populate_from='name')),
                ('name', models.CharField(help_text='This title will appear on the teaser card and on top of the project detail page. It should be max. 120 characters long', verbose_name='Title of your project', max_length=120)),
                ('description', models.CharField(help_text='This short description will appear on the header of the project and in the teaser. It should briefly state the goal of the project in max. 250 chars.', verbose_name='Short description of your project', max_length=250)),
                ('information', ckeditor_uploader.fields.RichTextUploadingField(help_text='This description should tell participants what the goal of the project is, how the project’s participation will look like. It will be always visible in the „Info“ tab on your project’s page.', verbose_name='Description of your project')),
                ('result', ckeditor_uploader.fields.RichTextUploadingField(help_text='Here you should explain what the expected outcome of the project will be and how you are planning to use the results. If the project is finished you should add a summary of the results.', blank=True)),
                ('is_public', models.BooleanField(help_text='Please indicate who should be able to participate in your project. Teasers for your project including title and short description will always be visible to everyone', verbose_name='Access to the project', default=True)),
                ('is_draft', models.BooleanField(default=True)),
                ('image', models.ImageField(verbose_name='Header image', blank=True, upload_to='projects/backgrounds', help_text='The image will be shown as a decorative background image. It must be min. 1300px wide and 600px tall. Allowed file formats are .jpg and .png. The file size should be max. 2 MB.')),
                ('moderators', models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='project_moderator')),
                ('organisation', models.ForeignKey(to=settings.A4_ORGANISATIONS_MODEL, on_delete=models.CASCADE)),
                ('participants', models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='project_participant', blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import adhocracy4.maps.fields
import django.db.models.deletion
import ckeditor.fields
import apps.moderatorfeedback.fields
import autoslug.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('a4categories', '__first__'),
        ('a4modules', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Proposal',
            fields=[
                ('item_ptr', models.OneToOneField(to='a4modules.Item', auto_created=True, serialize=False, parent_link=True, primary_key=True)),
                ('slug', autoslug.fields.AutoSlugField(unique=True, editable=False, populate_from='name')),
                ('name', models.CharField(max_length=120)),
                ('description', ckeditor.fields.RichTextField()),
                ('point', adhocracy4.maps.fields.PointField(help_text='Click inside marked area to set a marker. Drag and drop marker to change place.', verbose_name='Where can your idea be located on a map?')),
                ('budget', models.PositiveIntegerField(help_text='Required Budget', default=0)),
                ('moderator_feedback', apps.moderatorfeedback.fields.ModeratorFeedbackField(choices=[('CONSIDERATION', 'Under consideration'), ('REJECTED', 'Rejected'), ('ACCEPTED', 'Accepted')], null=True, blank=True, max_length=254, default=None)),
            ],
            options={
                'abstract': False,
            },
            bases=('a4modules.item', models.Model),
        ),
        migrations.CreateModel(
            name='ModeratorStatement',
            fields=[
                ('created', models.DateTimeField(editable=False, default=django.utils.timezone.now)),
                ('modified', models.DateTimeField(blank=True, null=True, editable=False)),
                ('proposal', models.OneToOneField(to='meinberlin_budgeting.Proposal', serialize=False, related_name='moderator_statement', primary_key=True)),
                ('statement', ckeditor.fields.RichTextField(blank=True)),
                ('creator', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='proposal',
            name='category',
            field=models.ForeignKey(to='a4categories.Category', on_delete=django.db.models.deletion.SET_NULL, null=True, blank=True),
        ),
    ]

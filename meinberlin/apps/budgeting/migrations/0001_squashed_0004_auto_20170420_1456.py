# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
from django.conf import settings
import autoslug.fields
import meinberlin.apps.moderatorfeedback.fields
import django.db.models.deletion
import ckeditor.fields
import adhocracy4.maps.fields


class Migration(migrations.Migration):

    replaces = [('meinberlin_budgeting', '0001_initial'), ('meinberlin_budgeting', '0002_proposal_moderator_feedback'), ('meinberlin_budgeting', '0003_moderatorstatement'), ('meinberlin_budgeting', '0004_auto_20170420_1456')]

    dependencies = [
        ('a4categories', '__first__'),
        ('a4modules', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Proposal',
            fields=[
                ('item_ptr', models.OneToOneField(serialize=False, auto_created=True, to='a4modules.Item', primary_key=True, parent_link=True)),
                ('slug', autoslug.fields.AutoSlugField(populate_from='name', editable=False, unique=True)),
                ('name', models.CharField(max_length=120)),
                ('description', ckeditor.fields.RichTextField()),
                ('budget', models.PositiveIntegerField(default=0, help_text='Required Budget')),
                ('category', models.ForeignKey(to='a4categories.Category', null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True)),
                ('moderator_feedback', meinberlin.apps.moderatorfeedback.fields.ModeratorFeedbackField(default=None, choices=[('CONSIDERATION', 'Under consideration'), ('REJECTED', 'Rejected'), ('ACCEPTED', 'Accepted')], null=True, blank=True, max_length=254)),
            ],
            options={
                'ordering': ['-created'],
                'abstract': False,
            },
            bases=('a4modules.item', models.Model),
        ),
        migrations.CreateModel(
            name='ModeratorStatement',
            fields=[
                ('created', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('modified', models.DateTimeField(blank=True, editable=False, null=True)),
                ('proposal', models.OneToOneField(serialize=False, related_name='moderator_statement', to='meinberlin_budgeting.Proposal', primary_key=True)),
                ('statement', ckeditor.fields.RichTextField(blank=True)),
                ('creator', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterModelOptions(
            name='proposal',
            options={},
        ),
        migrations.AddField(
            model_name='proposal',
            name='point',
            field=adhocracy4.maps.fields.PointField(default=None, verbose_name='Where can your idea be located on a map?', help_text='Click inside marked area to set a marker. Drag and drop marker to change place.'),
            preserve_default=False,
        ),
    ]

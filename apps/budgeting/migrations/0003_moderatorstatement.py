# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.utils.timezone
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('meinberlin_budgeting', '0002_proposal_moderator_feedback'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModeratorStatement',
            fields=[
                ('created', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('modified', models.DateTimeField(blank=True, null=True, editable=False)),
                ('proposal', models.OneToOneField(related_name='moderator_statement', primary_key=True, serialize=False, to='meinberlin_budgeting.Proposal')),
                ('statement', ckeditor.fields.RichTextField(blank=True)),
                ('creator', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

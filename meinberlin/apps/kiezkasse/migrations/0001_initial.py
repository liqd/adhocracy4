# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import ckeditor.fields
import autoslug.fields
import django.db.models.deletion
import adhocracy4.maps.fields


class Migration(migrations.Migration):

    dependencies = [
        ('a4modules', '0001_initial'),
        ('a4categories', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Proposal',
            fields=[
                ('item_ptr', models.OneToOneField(serialize=False, primary_key=True, to='a4modules.Item', parent_link=True, related_name='meinberlin_kiezkasse_proposal')),
                ('slug', autoslug.fields.AutoSlugField(populate_from='name', editable=False, unique=True)),
                ('name', models.CharField(max_length=120)),
                ('description', ckeditor.fields.RichTextField()),
                ('point', adhocracy4.maps.fields.PointField(verbose_name='Where can your idea be located on a map?', help_text='Click inside marked area to set a marker. Drag and drop marker to change place.')),
                ('point_label', models.CharField(max_length=255, verbose_name='Label of the ideas location', help_text='The label of the ideas location. This could be an address or the name of a landmark.', default='', blank=True)),
                ('budget', models.PositiveIntegerField(help_text='Required Budget', default=0)),
                ('creator_contribution', models.BooleanField(verbose_name='Own contribution to the project', help_text='I want to contribute to the project myself.', default=False)),
                ('category', models.ForeignKey(to='a4categories.Category', null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, related_name='+')),
            ],
            options={
                'abstract': False,
            },
            bases=('a4modules.item', models.Model),
        ),
    ]

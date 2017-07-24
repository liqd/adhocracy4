# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import adhocracy4.maps.fields
import autoslug.fields
import ckeditor.fields
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('a4modules', '0001_initial'),
        ('a4categories', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='MapIdea',
            fields=[
                ('item_ptr', models.OneToOneField(primary_key=True, serialize=False, auto_created=True, parent_link=True, to='a4modules.Item')),
                ('slug', autoslug.fields.AutoSlugField(unique=True, editable=False, populate_from='name')),
                ('name', models.CharField(max_length=120)),
                ('description', ckeditor.fields.RichTextField()),
                ('point', adhocracy4.maps.fields.PointField(verbose_name='Where can your idea be located on a map?', help_text='Click inside marked area to set a marker. Drag and drop marker to change place.')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='a4categories.Category')),
            ],
            options={
                'abstract': False,
            },
            bases=('a4modules.item', models.Model),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import ckeditor.fields
import django.db.models.deletion
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ('a4modules', '0001_initial'),
        ('a4categories', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Proposal',
            fields=[
                ('item_ptr', models.OneToOneField(primary_key=True, serialize=False, auto_created=True, parent_link=True, to='a4modules.Item')),
                ('slug', autoslug.fields.AutoSlugField(unique=True, editable=False, populate_from='name')),
                ('name', models.CharField(max_length=120)),
                ('description', ckeditor.fields.RichTextField()),
                ('budget', models.PositiveIntegerField(default=0, help_text='Required Budget')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='a4categories.Category')),
            ],
            options={
                'ordering': ['-created'],
                'abstract': False,
            },
            bases=('a4modules.item', models.Model),
        ),
    ]

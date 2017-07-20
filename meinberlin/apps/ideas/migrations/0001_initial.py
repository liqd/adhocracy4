# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import autoslug.fields
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('a4modules', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Idea',
            fields=[
                ('item_ptr', models.OneToOneField(primary_key=True, parent_link=True, to='a4modules.Item', auto_created=True, serialize=False)),
                ('slug', autoslug.fields.AutoSlugField(unique=True, populate_from='name', editable=False)),
                ('name', models.CharField(max_length=120)),
                ('description', ckeditor.fields.RichTextField()),
            ],
            options={
                'abstract': False,
            },
            bases=('a4modules.item',),
        ),
    ]

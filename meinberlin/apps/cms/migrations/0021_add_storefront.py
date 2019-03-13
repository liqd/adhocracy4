# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-10-24 14:36
from __future__ import unicode_literals

import django.db.models.deletion
import modelcluster.fields
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0040_page_draft_title'),
        ('meinberlin_cms', '0020_add_header_block'),
    ]

    operations = [
        migrations.CreateModel(
            name='Storefront',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StorefrontItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
            ],
        ),
        migrations.AlterField(
            model_name='homepage',
            name='header_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='meinberlin_cms.CustomImage'),
        ),
        migrations.CreateModel(
            name='StorefrontCollection',
            fields=[
                ('storefrontitem_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='meinberlin_cms.StorefrontItem')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('parent', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='meinberlin_cms.Storefront')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
            bases=('meinberlin_cms.storefrontitem', models.Model),
        ),
        migrations.AddField(
            model_name='storefrontitem',
            name='header_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='meinberlin_cms.CustomImage'),
        ),
        migrations.AddField(
            model_name='storefrontitem',
            name='link_page',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wagtailcore.Page'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='storefront',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='meinberlin_cms.Storefront'),
        ),
    ]

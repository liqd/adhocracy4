# -*- coding: utf-8 -*-
import modelcluster.fields
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0030_index_on_pagerevision_created_at'),
        ('cms', '0002_homepage_body'),
    ]

    operations = [
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('title', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='NavigationMenu',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('title', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='NavigationMenuItem',
            fields=[
                ('menuitem_ptr', models.OneToOneField(to='cms.MenuItem', serialize=False, parent_link=True, primary_key=True, auto_created=True)),
                ('sort_order', models.IntegerField(null=True, blank=True, editable=False)),
                ('parent', modelcluster.fields.ParentalKey(to='cms.NavigationMenu', related_name='items')),
            ],
            options={
                'abstract': False,
                'ordering': ['sort_order'],
            },
            bases=('cms.menuitem', models.Model),
        ),
        migrations.AddField(
            model_name='menuitem',
            name='link_page',
            field=models.ForeignKey(to='wagtailcore.Page'),
        ),
    ]

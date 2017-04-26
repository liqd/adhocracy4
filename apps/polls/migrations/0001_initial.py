# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('a4modules', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('label', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('item_ptr', models.OneToOneField(to='a4modules.Item', serialize=False, auto_created=True, primary_key=True, parent_link=True)),
                ('title', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
            bases=('a4modules.item',),
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(editable=False, default=django.utils.timezone.now)),
                ('modified', models.DateTimeField(blank=True, editable=False, null=True)),
                ('choice', models.ForeignKey(to='meinberlin_polls.Choice')),
                ('creator', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='choice',
            name='poll',
            field=models.ForeignKey(to='meinberlin_polls.Poll'),
        ),
        migrations.AlterUniqueTogether(
            name='vote',
            unique_together=set([('creator', 'choice')]),
        ),
    ]

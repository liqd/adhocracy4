# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('a4modules', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('label', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('item_ptr', models.OneToOneField(primary_key=True, to='a4modules.Item', serialize=False, parent_link=True, auto_created=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('a4modules.item',),
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('label', models.CharField(max_length=255)),
                ('weight', models.SmallIntegerField()),
                ('poll', models.ForeignKey(related_name='questions', to='a4polls.Poll')),
            ],
            options={
                'ordering': ['weight'],
            },
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('created', models.DateTimeField(editable=False, default=django.utils.timezone.now)),
                ('modified', models.DateTimeField(null=True, blank=True, editable=False)),
                ('choice', models.ForeignKey(related_name='votes', to='a4polls.Choice')),
                ('creator', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='choice',
            name='question',
            field=models.ForeignKey(related_name='choices', to='a4polls.Question'),
        ),
        migrations.AlterUniqueTogether(
            name='vote',
            unique_together=set([('creator', 'choice')]),
        ),
    ]

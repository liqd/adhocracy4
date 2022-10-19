# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import modelcluster.fields
import wagtail.fields
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0032_add_bulk_delete_page_permission'),
        ('meinberlin_cms', '0004_add_projects_block'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailFormField',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('sort_order', models.IntegerField(blank=True, null=True, editable=False)),
                ('label', models.CharField(verbose_name='label', max_length=255, help_text='The label of the form field')),
                ('field_type', models.CharField(verbose_name='field type', max_length=16, choices=[('singleline', 'Single line text'), ('multiline', 'Multi-line text'), ('email', 'Email'), ('number', 'Number'), ('url', 'URL'), ('checkbox', 'Checkbox'), ('checkboxes', 'Checkboxes'), ('dropdown', 'Drop down'), ('radio', 'Radio buttons'), ('date', 'Date'), ('datetime', 'Date/time')])),
                ('required', models.BooleanField(verbose_name='required', default=True)),
                ('choices', models.TextField(verbose_name='choices', blank=True, help_text='Comma separated list of choices. Only applicable in checkboxes, radio and dropdown.')),
                ('default_value', models.CharField(verbose_name='default value', max_length=255, blank=True, help_text='Default value. Comma separated values supported for checkboxes.')),
                ('help_text', models.CharField(verbose_name='help text', max_length=255, blank=True)),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EmailFormPage',
            fields=[
                ('page_ptr', models.OneToOneField(primary_key=True, serialize=False, auto_created=True, parent_link=True, to='wagtailcore.Page', on_delete=models.CASCADE)),
                ('to_address', models.CharField(verbose_name='to address', max_length=255, blank=True, help_text='Optional - form submissions will be emailed to these addresses. Separate multiple addresses by comma.')),
                ('from_address', models.CharField(verbose_name='from address', max_length=255, blank=True)),
                ('subject', models.CharField(verbose_name='subject', max_length=255, blank=True)),
                ('intro', wagtail.fields.RichTextField(help_text='Introduction text shown above the form')),
                ('thank_you', wagtail.fields.RichTextField(help_text='Text shown after form submission')),
                ('email_content', models.CharField(max_length=200, help_text='Email content message')),
                ('attach_as', models.CharField(max_length=3, default='csv', choices=[('csv', 'CSV Document')], help_text='Form results are send in this document format')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.AddField(
            model_name='emailformfield',
            name='page',
            field=modelcluster.fields.ParentalKey(related_name='form_fields', to='meinberlin_cms.EmailFormPage'),
        ),
    ]

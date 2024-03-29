# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-07-16 07:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("a4projects", "0015_add_contact_fields"),
    ]

    operations = [
        migrations.AlterField(
            model_name="project",
            name="contact_address_text",
            field=models.TextField(blank=True, verbose_name="Postal address"),
        ),
        migrations.AlterField(
            model_name="project",
            name="contact_name",
            field=models.CharField(
                blank=True, max_length=120, verbose_name="Contact person"
            ),
        ),
    ]

# Generated by Django 4.2 on 2024-01-30 10:03

import adhocracy4.images.validators
from django.db import migrations
import django_ckeditor_5.fields


class Migration(migrations.Migration):
    dependencies = [
        ("a4projects", "0045_rename_field_m2mtopics_to_topics"),
    ]

    operations = [
        migrations.AlterField(
            model_name="project",
            name="information",
            field=django_ckeditor_5.fields.CKEditor5Field(
                blank=True,
                validators=[adhocracy4.images.validators.ImageAltTextValidator()],
                verbose_name="Description of your project",
            ),
        ),
        migrations.AlterField(
            model_name="project",
            name="result",
            field=django_ckeditor_5.fields.CKEditor5Field(
                blank=True,
                validators=[adhocracy4.images.validators.ImageAltTextValidator()],
                verbose_name="Results of your project",
            ),
        ),
    ]
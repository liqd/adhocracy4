# Generated by Django 4.2 on 2024-01-29 13:29

import adhocracy4.images.validators
from django.db import migrations
import django_ckeditor_5.fields


class Migration(migrations.Migration):
    dependencies = [
        ("a4projects", "0046_alter_project_information_alter_project_result"),
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

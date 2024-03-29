# Generated by Django 3.2.20 on 2023-09-19 09:52

from django.db import migrations
import django_ckeditor_5.fields


class Migration(migrations.Migration):
    dependencies = [
        ("a4projects", "0039_add_alt_text_to_field"),
    ]

    operations = [
        migrations.AlterField(
            model_name="project",
            name="information",
            field=django_ckeditor_5.fields.CKEditor5Field(
                blank=True,
                help_text="This description should tell participants what the goal of the project is, how the project’s participation will look like. It will be always visible in the „Info“ tab on your project’s page.",
                verbose_name="Description of your project",
            ),
        ),
        migrations.AlterField(
            model_name="project",
            name="result",
            field=django_ckeditor_5.fields.CKEditor5Field(
                blank=True,
                help_text="Here you should explain what the expected outcome of the project will be and how you are planning to use the results. If the project is finished you should add a summary of the results.",
                verbose_name="Results of your project",
            ),
        ),
    ]

# Generated by Django 4.2 on 2023-11-29 15:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("a4projects", "0044_remove_project_field_topics"),
    ]

    operations = [
        migrations.RenameField(
            model_name="project", old_name="m2mtopics", new_name="topics"
        ),
    ]
# Generated by Django 2.2.16 on 2020-10-21 13:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("a4projects", "0029_is_public_to_access"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="project",
            name="is_public",
        ),
    ]

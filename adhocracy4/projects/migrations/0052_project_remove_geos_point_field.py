# Generated by Django 4.2.17 on 2025-02-19 15:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("a4projects", "0052_migrate_point_field"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="project",
            name="geos_point",
        ),
    ]

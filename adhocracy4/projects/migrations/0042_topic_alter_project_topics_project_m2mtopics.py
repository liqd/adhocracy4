# Generated by Django 4.2 on 2023-11-29 13:18

import adhocracy4.projects.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("a4projects", "0041_ckeditor5_iframes"),
    ]

    operations = [
        migrations.CreateModel(
            name="Topic",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("code", models.CharField(blank=True, max_length=10)),
                ("name", models.CharField(max_length=120, verbose_name="Topic")),
            ],
        ),
        migrations.AddField(
            model_name="project",
            name="m2mtopics",
            field=models.ManyToManyField(to="a4projects.topic"),
        ),
    ]

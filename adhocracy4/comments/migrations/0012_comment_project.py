# Generated by Django 3.2.19 on 2023-06-06 13:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("a4projects", "0038_verbose_name_created_modified"),
        ("a4comments", "0011_comment_is_reviewed"),
    ]

    operations = [
        migrations.AddField(
            model_name="comment",
            name="project",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="a4projects.project",
            ),
        ),
    ]

# Generated by Django 3.2.16 on 2023-04-06 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("a4comments", "0010_verbose_name_created_modified"),
    ]

    operations = [
        migrations.AddField(
            model_name="comment",
            name="is_reviewed",
            field=models.BooleanField(default=False),
        ),
    ]

# Generated by Django 4.2 on 2023-11-27 12:54

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("a4comments", "0013_set_project"),
    ]

    operations = [
        migrations.RenameIndex(
            model_name="comment",
            new_name="a4comments__content_ff606b_idx",
            old_fields=("content_type", "object_pk"),
        ),
    ]
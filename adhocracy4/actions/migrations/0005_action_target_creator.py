# Generated by Django 3.2.19 on 2023-05-25 08:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("a4actions", "0004_auto_20181204_1650"),
    ]

    operations = [
        migrations.AddField(
            model_name="action",
            name="target_creator",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="target_creator",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]

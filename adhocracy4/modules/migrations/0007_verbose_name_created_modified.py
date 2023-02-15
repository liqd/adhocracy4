# Generated by Django 3.2.17 on 2023-02-15 08:40

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("a4modules", "0006_module_blueprint_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="item",
            name="created",
            field=models.DateTimeField(
                default=django.utils.timezone.now,
                editable=False,
                verbose_name="Created",
            ),
        ),
        migrations.AlterField(
            model_name="item",
            name="modified",
            field=models.DateTimeField(
                blank=True, editable=False, null=True, verbose_name="Modified"
            ),
        ),
    ]

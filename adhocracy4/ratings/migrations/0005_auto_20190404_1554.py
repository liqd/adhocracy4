# Generated by Django 2.2 on 2019-04-04 15:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('a4ratings', '0004_auto_20190404_1512'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='content_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType'),
        ),
    ]

# Generated by Django 2.2.24 on 2021-09-24 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a4test_questions', '0004_alter_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='last_discussed',
            field=models.DateTimeField(blank=True, editable=False, null=True),
        ),
    ]
# Generated by Django 4.2 on 2024-04-02 18:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("a4labels", "0003_labelalias"),
        ("a4test_ideas", "0006_alter_idea_description"),
    ]

    operations = [
        migrations.AlterField(
            model_name="idea",
            name="labels",
            field=models.ManyToManyField(
                related_name="%(app_label)s_%(class)s_label", to="a4labels.label"
            ),
        ),
    ]

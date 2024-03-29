# Generated by Django 2.2.24 on 2021-07-09 11:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("moderatorfeedback", "__first__"),
        ("a4test_ideas", "0002_idea_labels"),
    ]

    operations = [
        migrations.AddField(
            model_name="idea",
            name="moderator_feedback",
            field=models.CharField(blank=True, max_length=256),
        ),
        migrations.AddField(
            model_name="idea",
            name="moderator_statement",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="+",
                to="moderatorfeedback.ModeratorStatement",
            ),
        ),
    ]

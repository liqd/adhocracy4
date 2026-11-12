from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    dependencies = [
        ("a4polls", "0013_alter_answer_answer"),
    ]

    operations = [
        migrations.AddField(
            model_name="poll",
            name="presentation_mode",
            field=models.CharField(
                choices=[
                    ("multistep", "One question per step"),
                    ("longform", "All questions on one page"),
                ],
                default="multistep",
                max_length=20,
                verbose_name="Presentation",
            ),
        ),
    ]

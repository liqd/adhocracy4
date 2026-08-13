from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("a4polls", "0011_alter_question_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="poll",
            name="hide_results_until_finished",
            field=models.BooleanField(
                default=False,
                verbose_name="Hide results until participation is over",
            ),
        ),
    ]

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("a4polls", "0007_alter_poll_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="question",
            name="is_confidential",
            field=models.BooleanField(
                default=False,
                help_text=(
                    "Individual responses are not shown publicly; only the number of "
                    "submissions is visible."
                ),
                verbose_name="Confidential answers",
            ),
        ),
    ]

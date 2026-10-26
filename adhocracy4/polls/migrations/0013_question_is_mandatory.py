from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("a4polls", "0012_poll_hide_results_until_finished"),
    ]

    operations = [
        migrations.AddField(
            model_name="question",
            name="is_mandatory",
            field=models.BooleanField(
                default=False,
                help_text=(
                    "Participants have to answer this question before submitting."
                ),
                verbose_name="Mandatory question",
            ),
        ),
    ]

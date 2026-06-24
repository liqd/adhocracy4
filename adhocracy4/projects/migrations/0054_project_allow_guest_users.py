from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("a4projects", "0053_alter_project_description"),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="allow_guest_users",
            field=models.BooleanField(
                default=True,
                help_text=(
                    "Whether guest users may participate in this project. "
                    "Only applies when guest users are enabled for the platform."
                ),
                verbose_name="Allow guest users to participate",
            ),
        ),
    ]

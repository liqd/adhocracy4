from django.db import migrations, models


def disallow_guest_users_on_existing_projects(apps, schema_editor):
    Project = apps.get_model("a4projects", "Project")
    Project.objects.update(allow_guest_users=False)


class Migration(migrations.Migration):

    dependencies = [
        ("a4projects", "0054_project_allow_guest_users"),
    ]

    operations = [
        migrations.RunPython(
            disallow_guest_users_on_existing_projects,
            migrations.RunPython.noop,
        ),
        migrations.AlterField(
            model_name="project",
            name="allow_guest_users",
            field=models.BooleanField(
                default=False,
                help_text=(
                    "Whether guest users may participate in this project. "
                    "Only applies when guest users are enabled for the platform."
                ),
                verbose_name="Allow guest users to participate",
            ),
        ),
    ]

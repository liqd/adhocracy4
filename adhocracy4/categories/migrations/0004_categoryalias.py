# Generated by Django 3.2.19 on 2023-06-02 12:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("a4modules", "0007_verbose_name_created_modified"),
        ("a4categories", "0003_alter_category_options"),
    ]

    operations = [
        migrations.CreateModel(
            name="CategoryAlias",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        default="Category",
                        help_text="You can individualise the term category. The character limit is max. 25 characters (with spaces).",
                        max_length=25,
                        verbose_name="Type of category",
                    ),
                ),
                (
                    "description",
                    models.CharField(
                        default="Assign your proposal to a category. This automatically appears in the display of your proposal. The list of all proposals can be filtered by category.",
                        help_text="You can individualise the description text. The description text is displayed to the participants as help text when they have to assign their ideas. The character limit is max. 300 characters (with spaces).",
                        max_length=300,
                        verbose_name="Description/Helptext",
                    ),
                ),
                (
                    "module",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="a4modules.module",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "categorie alias",
                "ordering": ["pk"],
            },
        ),
    ]

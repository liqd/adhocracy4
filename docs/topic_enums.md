# A4 Project Topics

## Introduction
Each project has the option to choose up to two topics relevant to the project's context. For the choises of topics we used to work with a list of tuples defined in the settings directly, and the django-multiselectfield library, but we needed to replace this library as it is no longer maintained. So a `Project` object now has a many-to-many relation with `topics`, and `Topic` objects are created based on the `TopicEnum` class. Enums are also more flexible to work with, as we can call the enum values, label and code properties depending on where and how these are called in the code.

## Configuration
The topics should be defined in the settings as a string path to an Enum class (TopicEnum):
```
A4_PROJECT_TOPICS = "tests.project.enums.TopicEnum"
```
[ref: tests/project/settings](https://github.com/liqd/adhocracy4/blob/main/tests/project/settings.py)

## Development

`Project` property `topic_names` has now changed to accommodate the new TopicEnum class, mostly for html template use.  
[ref: Topic/Project/topic_names](https://github.com/liqd/adhocracy4/blob/main/adhocracy4/projects/models.py)

## Migration
If a django application which is based on `adhocracy4` has projects with existing topics and using the django-multiselectfield, those will be added to a many-to-many topics field after updating `adhocracy4` and run the migrations. Your django application would need to define a TopicEnum and define its path as a string in the settings like the example in the configuration section above. The previous tuples for topic choices that used to be, for example, in the form of:
```
A4_PROJECT_TOPICS = (
    ("ANT", _("Anti-discrimination")),
    ("WOR", _("Work & economy")),
    ("BUI", _("Building & living")),
)
```
will now need to move to an Enum class in your django application, or also possible to move to django's `models.TextChoices`, which is a subclass of Enum and allows for applying dynamic translations for the labels with gettext `_` as in the following example:
```
class TopicEnum(models.TextChoices):
    """Choices for project topics."""

    ANT = "ANT", _("Anti-discrimination"),
    WOR = "WOR", _("Work & economy"),
    BUI = "BUI", _("Building & living")
```

Once this is done, your django application needs to make these enums as `Topic` objects with a custom migration. Generate an empty migration with `python manage.py makemigrations <app_name> --empty`. Edit the new migration. Here some boilerplate code for such a migration:
```
from my_application.apps.projects.enums import TopicEnum


def add_topics(apps, schema_editor):
    if hasattr(settings, "A4_PROJECT_TOPICS"):
        Topic = apps.get_model("a4projects", "Topic")
        for topic in TopicEnum:
            Topic.objects.get_or_create(code=topic)


class Migration(migrations.Migration):
    dependencies = [
        ("app_label", "xxxx_previous_migration"),
    ]

    operations = [
        migrations.RunPython(add_topics, migrations.RunPython.noop),
    ]
```

# Generated by Django 4.2 on 2023-11-29 13:20

from django.db import migrations
from django.conf import settings


def add_topics_to_m2m_table(apps, schema_editor):
    if hasattr(settings, "A4_PROJECT_TOPICS"):
        topicsenum = settings.A4_PROJECT_TOPICS
        project = apps.get_model("a4projects", "Project")
        for project in project.objects.all():
            for topic_code in project.topics:
                project.m2mtopics.create(
                    code=topic_code,
                    name=[item[1] for item in topicsenum if item[0] == topic_code][0],
                )
    else:
        pass


def reverse_func(apps, schema_editor):
    if hasattr(settings, "A4_PROJECT_TOPICS"):
        project = apps.get_model("a4projects", "Project")
        for project in project.objects.all():
            for topic in project.m2mtopics.all():
                project.m2mtopics.remove(topic)
    else:
        pass


class Migration(migrations.Migration):
    dependencies = [
        ("a4projects", "0042_topic_alter_project_topics_project_m2mtopics"),
    ]

    operations = [
        migrations.RunPython(add_topics_to_m2m_table, reverse_func),
    ]

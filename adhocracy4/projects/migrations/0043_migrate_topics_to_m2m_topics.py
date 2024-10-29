# Generated by Django 4.2 on 2023-11-29 13:20
import logging

from django.db import migrations
from django.conf import settings


logger = logging.getLogger(__name__)


def add_topics_to_m2m_table(apps, schema_editor):
    if hasattr(settings, "A4_PROJECT_TOPICS"):
        project = apps.get_model("a4projects", "Project")
        topic = apps.get_model("a4projects", "Topic")
        for project in project.objects.all():
            try:
                for topic_code in project.topics.split(","):
                    if not topic_code:
                        continue
                    if len(topic_code) > 10:
                        logger.warning(
                            "warning: dropping too long topic:"
                            + topic_code
                            + ". Max length is 10"
                        )
                        continue
                    proj_topic, _ = topic.objects.get_or_create(
                        code=topic_code,
                    )
                    project.m2mtopics.add(proj_topic)
            except Exception as e:
                logger.warning(
                    "error migrating topics for project " + project.name + ": " + str(e)
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
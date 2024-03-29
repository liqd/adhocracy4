# Generated by Django 3.2.19 on 2023-05-25 08:22
from django.contrib.contenttypes.models import ContentType
from django.db import migrations, transaction

BATCH_SIZE = 10000


def set_comment_project(apps, schema_editor):
    Comment = apps.get_model("a4comments", "Comment")
    comments = []
    count = 0
    for comment in Comment.objects.all().iterator(chunk_size=BATCH_SIZE):
        content_object = _get_content_object(apps, Comment, comment)
        if hasattr(content_object, "module"):
            comment.project = content_object.module.project
            comments.append(comment)
            count += 1
        if count == BATCH_SIZE:
            Comment.objects.bulk_update(comments, ["project"])
            count = 0
    if count != 0:
        Comment.objects.bulk_update(comments, ["project"])


def _get_content_object(apps, Comment, comment):
    model = apps.get_model(
        app_label=comment.content_type.app_label,
        model_name=comment.content_type.model,
    )
    content_object = model.objects.get(id=comment.object_pk)
    if isinstance(content_object, Comment):
        return _get_content_object(apps, Comment, content_object)
    elif hasattr(content_object, "chapter"):
        return content_object.chapter
    return content_object


def clear_comment_project(apps, schema_editor):
    Comment = apps.get_model("a4comments", "Comment")
    Comment.objects.exclude(project__isnull=True).update(project=None)


class Migration(migrations.Migration):
    dependencies = [
        ("a4comments", "0012_comment_project"),
    ]

    operations = [
        migrations.RunPython(
            set_comment_project,
            reverse_code=clear_comment_project,
            atomic=False,
        )
    ]

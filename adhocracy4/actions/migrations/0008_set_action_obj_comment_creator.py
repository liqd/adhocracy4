# Generated by Django 3.2.19 on 2023-05-25 08:22
from django.contrib.contenttypes.models import ContentType
from django.db import migrations, transaction

BATCH_SIZE = 10000


def set_action_obj_comment_creator(apps, schema_editor):
    Action = apps.get_model("a4actions", "Action")
    actions = []
    count = 0
    for action in Action.objects.all().iterator(chunk_size=BATCH_SIZE):
        if not action.obj_object_id:
            continue
        model = apps.get_model(
            app_label=action.obj_content_type.app_label,
            model_name=action.obj_content_type.model,
        )
        try:
            content_object = model.objects.get(id=action.obj_object_id)
            if hasattr(content_object, "comment") and hasattr(
                content_object.comment, "creator"
            ):
                action.obj_comment_creator = content_object.comment.creator
                actions.append(action)
                count += 1
        except model.DoesNotExist:
            pass
        if count == BATCH_SIZE:
            Action.objects.bulk_update(actions, ["obj_comment_creator_creator"])
            count = 0
            actions = []
    if count != 0:
        Action.objects.bulk_update(actions, ["obj_comment_creator"])


def clear_action_obj_comment_creator(apps, schema_editor):
    Action = apps.get_model("a4actions", "Action")
    Action.objects.exclude(obj_comment_creator__isnull=True).update(
        obj_comment_creator=None
    )


class Migration(migrations.Migration):
    dependencies = [
        ("a4actions", "0007_action_obj_comment_creator"),
    ]

    operations = [
        migrations.RunPython(
            set_action_obj_comment_creator,
            reverse_code=clear_action_obj_comment_creator,
            atomic=False,
        )
    ]
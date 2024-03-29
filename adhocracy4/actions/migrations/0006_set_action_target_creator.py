# Generated by Django 3.2.19 on 2023-05-25 08:22

from django.db import migrations, transaction

BATCH_SIZE = 10000


def set_action_target_creator(apps, schema_editor):
    Action = apps.get_model("a4actions", "Action")
    actions = []
    count = 0
    for action in Action.objects.filter(verb="add").iterator(chunk_size=BATCH_SIZE):
        model = apps.get_model(
            app_label=action.target_content_type.app_label,
            model_name=action.target_content_type.model,
        )
        try:
            content_object = model.objects.get(id=action.target_object_id)
            if hasattr(content_object, "creator"):
                action.target_creator = content_object.creator
                actions.append(action)
                count += 1
        except model.DoesNotExist:
            pass
        if count == BATCH_SIZE:
            Action.objects.bulk_update(actions, ["target_creator"])
            count = 0
            actions = []
    if count != 0:
        Action.objects.bulk_update(actions, ["target_creator"])


def clear_action_target_creator(apps, schema_editor):
    Action = apps.get_model("a4actions", "Action")
    Action.objects.filter(verb="add").exclude(target_creator__isnull=True).update(
        target_creator=None
    )


class Migration(migrations.Migration):
    dependencies = [
        ("a4actions", "0005_action_target_creator"),
    ]

    operations = [
        migrations.RunPython(
            set_action_target_creator,
            reverse_code=clear_action_target_creator,
            atomic=False,
        )
    ]

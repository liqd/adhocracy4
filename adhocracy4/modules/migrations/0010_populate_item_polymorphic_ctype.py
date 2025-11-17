# Generated manually to backfill polymorphic_ctype on existing items.
from django.db import migrations


def populate_polymorphic_ctypes(apps, schema_editor):
    Item = apps.get_model("a4modules", "Item")
    ContentType = apps.get_model("contenttypes", "ContentType")
    db_alias = schema_editor.connection.alias

    def get_parent_link(model):
        for field in model._meta.fields:
            remote_field = getattr(field, "remote_field", None)
            if remote_field and remote_field.parent_link:
                return field
        return None

    # Update all known subclasses first.
    for model in apps.get_models():
        if model is Item:
            continue
        try:
            is_item_subclass = issubclass(model, Item)
        except TypeError:
            continue
        if not is_item_subclass:
            continue

        parent_link_field = get_parent_link(model)
        if not parent_link_field:
            continue

        content_type = ContentType.objects.db_manager(db_alias).get_for_model(
            model, for_concrete_model=False
        )
        item_ids = model._default_manager.using(db_alias).values_list(
            parent_link_field.attname, flat=True
        )
        (
            Item.objects.using(db_alias)
            .filter(polymorphic_ctype__isnull=True, pk__in=item_ids)
            .update(polymorphic_ctype=content_type)
        )

    # Any remaining items fallback to the base Item content type.
    base_ct = ContentType.objects.db_manager(db_alias).get_for_model(
        Item, for_concrete_model=False
    )
    (
        Item.objects.using(db_alias)
        .filter(polymorphic_ctype__isnull=True)
        .update(polymorphic_ctype=base_ct)
    )


def remove_polymorphic_ctypes(apps, schema_editor):
    Item = apps.get_model("a4modules", "Item")
    Item.objects.using(schema_editor.connection.alias).update(polymorphic_ctype=None)


class Migration(migrations.Migration):
    dependencies = [
        ("a4modules", "0009_alter_item_options_item_polymorphic_ctype"),
    ]

    operations = [
        migrations.RunPython(
            populate_polymorphic_ctypes, reverse_code=remove_polymorphic_ctypes
        ),
    ]

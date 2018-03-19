from django.apps import apps
from django.db.models.signals import post_delete, post_init, post_save

from .fields import ConfiguredFileField

_PREFIX = '_a4files_'
_FILE_FIELDS_ATTR = _PREFIX + 'file_fields'
_CURRENT_FILES_ATTR = _PREFIX + 'current_files'


def backup_files_path_on_init(sender, instance, **kwargs):
    backup_files_path(instance)


def backup_files_path(instance):
    file_fields = getattr(instance, _FILE_FIELDS_ATTR, [])
    current_files = [getattr(instance, fieldname)
                     for fieldname in file_fields]
    setattr(instance, _CURRENT_FILES_ATTR, current_files)


def delete_old_files_on_save(sender, instance, **kwargs):
    file_fields = getattr(instance, _FILE_FIELDS_ATTR, [])
    current_files = getattr(instance, _CURRENT_FILES_ATTR, ())

    delete_files = [current_file
                    for fieldname, current_file
                    in zip(file_fields, current_files)
                    if getattr(instance, fieldname, None) != current_file]
    for file in delete_files:
        file.delete(False)

    backup_files_path(instance)


def delete_files_cascaded(sender, instance, **kwargs):
    file_fields = getattr(instance, _FILE_FIELDS_ATTR, [])
    files = [getattr(instance, fieldname) for fieldname in file_fields]
    for file in files:
        file.delete(False)


# Setup signals for all ConfiguredFileFields
for model in apps.get_models():
    for field in model._meta.get_fields(include_parents=False):
        if isinstance(field, ConfiguredFileField):
            file_fields = getattr(model, _FILE_FIELDS_ATTR, [])
            if field.attname not in file_fields:
                file_fields.append(field.attname)
                setattr(model, _FILE_FIELDS_ATTR, file_fields)

    if hasattr(model, _FILE_FIELDS_ATTR):
        post_init.connect(backup_files_path_on_init, sender=model)
        post_save.connect(delete_old_files_on_save, sender=model)
        post_delete.connect(delete_files_cascaded, sender=model)

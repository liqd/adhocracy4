from django import dispatch
from django.apps import apps
from django.db.models import signals as db_signals

from adhocracy4.modules.models import Module
from adhocracy4.projects.models import Project

project_created = dispatch.Signal(providing_args=['project'])
module_created = dispatch.Signal(providing_args=['module'])
# Handlers may return an error message to prevent a project from publishing
project_pre_publish = dispatch.Signal(providing_args=['project'])
project_published = dispatch.Signal(providing_args=['project'])
project_unpublished = dispatch.Signal(providing_args=['project'])
project_archived = dispatch.Signal(providing_args=['project'])


def _handle_project_signal(sender, instance, created, *args, **kwargs):
    if created:
        project_created.send(sender=None, project=instance)


def _handle_module_signal(sender, instance, created, *args, **kwargs):
    if created:
        module_created.send(sender=None, module=instance)


def connect_model_signal_handlers():
    # Setup signals for all Models inheriting from Project
    for model in apps.get_models():
        if issubclass(model, Project):
            db_signals.post_save.connect(_handle_project_signal, sender=model)

    # Setup signals for Modules
    db_signals.post_save.connect(_handle_module_signal, sender=Module)

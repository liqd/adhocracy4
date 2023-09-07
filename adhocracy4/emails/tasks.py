import importlib

from celery import shared_task
from django.apps import apps


@shared_task
def send_async(
    email_module_name, email_class_name, app_label, model_name, object_pk, args, kwargs
):
    imported_module = importlib.import_module(email_module_name)
    cls = getattr(imported_module, email_class_name)
    model = apps.get_model(app_label, model_name)
    obj = model.objects.get(pk=object_pk)

    return cls().dispatch(obj, *args, **kwargs)

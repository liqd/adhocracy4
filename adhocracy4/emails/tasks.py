import importlib

from background_task import background
from django.apps import apps


@background(schedule=1)
def send_async(email_module_name, email_class_name,
               app_label, model_name, object_pk,
               args, kwargs):
    mod = importlib.import_module(email_module_name)
    cls = getattr(mod, email_class_name)
    model = apps.get_model(app_label, model_name)
    object = model.objects.get(pk=object_pk)
    return cls().dispatch(object, *args, **kwargs)

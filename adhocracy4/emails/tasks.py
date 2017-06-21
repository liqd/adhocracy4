from django.apps import apps
import importlib
from background_task import background


@background(schedule=1)
def send_async(email_module_name, email_class_name,
               app_label, model_name, object_id,
               *args, **kwargs):
    mod = importlib.import_module(email_module_name)
    cls = getattr(mod, email_class_name)
    model = apps.get_model(app_label, model_name)
    object = model.objects.get(id=object_id)
    return cls().dispatch(object, *args, **kwargs)

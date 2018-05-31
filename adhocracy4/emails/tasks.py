from django.apps import apps
import importlib
import pickle
from base64 import b64encode, b64decode
from background_task import background


@background(schedule=1)
def send_async(email_module_name, email_class_name,
               app_label, model_name, object_pk,
               args, kwargs):
    mod = importlib.import_module(email_module_name)
    cls = getattr(mod, email_class_name)
    model = apps.get_model(app_label, model_name)
    object = model.objects.get(pk=object_pk)
    return cls().dispatch(object, *args, **kwargs)


@background(schedule=1)
def send_single_mail_task(encoded_mail):
    mail = pickle.loads(b64decode(encoded_mail))
    mail.send()

def send_single_mail(mail, *args, **kwargs):
    pickled_mail = pickle.dumps(mail)
    encoded_mail = b64encode(pickled_mail).decode()
    send_single_mail_task(encoded_mail, *args, **kwargs)

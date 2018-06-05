from django.apps import apps
import importlib
import pickle
from base64 import b64encode, b64decode
from background_task import background


@background(schedule=1)
def send_async(email_module_name, email_class_name, app_label, model_name,
               object_pk, args, kwargs):
    mod = importlib.import_module(email_module_name)
    cls = getattr(mod, email_class_name)
    model = apps.get_model(app_label, model_name)
    object = model.objects.get(pk=object_pk)
    return cls().dispatch(object, *args, **kwargs)


def serialize_email(email_obj):
    pickled_email = pickle.dumps(email_obj)
    return b64encode(pickled_email).decode()


def deserialize_email(email_string):
    return pickle.loads(b64decode(email_string))


@background(schedule=1)
def send_single_mail_task(encoded_mail):
    mail = deserialize_email(encoded_mail)
    mail.send()


def send_single_mail(email, *args, **kwargs):
    send_single_mail_task(
                          serialize_email(email),
                          *args,
                          **kwargs)

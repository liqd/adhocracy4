from .test import *

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "USER": "postgres",
        "NAME": "django",
        "TEST": {"NAME": "django_test"},
    }
}

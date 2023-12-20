from .test import *

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
    }
}

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "USER": "postgres",
        "NAME": "django",
        "TEST": {"NAME": "django_test"},
    }
}

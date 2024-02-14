from celery.schedules import crontab

from .base import *

DEBUG = False

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",  # defaut is 0 and is taken by celery for backend results
        "TIMEOUT": 86400,  # 24hrs
    }
}

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

try:
    from .local import *
except ImportError:
    pass

try:
    from .polygons import *
except ImportError:
    pass

try:
    INSTALLED_APPS += tuple(ADDITIONAL_APPS)
except NameError:
    pass

try:
    CKEDITOR_CONFIGS["collapsible-image-editor"]["embed_provider"] = CKEDITOR_URL
    CKEDITOR_CONFIGS["video-editor"]["embed_provider"] = CKEDITOR_URL
except NameError:
    pass

CELERY_BEAT_SCHEDULE = {
    "update-cache-for-projects-every-10-mim": {
        "task": "schedule_reset_cache_for_projects",
        "schedule": crontab(minute="*/10"),
        "args": (),
    },
}

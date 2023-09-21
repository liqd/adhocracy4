from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

for template_engine in TEMPLATES:
    template_engine["OPTIONS"]["debug"] = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "qid$h1o8&wh#p(j)lifis*5-rf@lbiy8%^3l4x%@b$z(tli@ab"

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
    }
}

CELERY_TASK_ALWAYS_EAGER = True

try:
    import debug_toolbar
except ImportError:
    pass
else:
    INSTALLED_APPS += (
        "debug_toolbar",
        "meinberlin.apps.dev",
    )
    MIDDLEWARE += ("debug_toolbar.middleware.DebugToolbarMiddleware",)
    INTERNAL_IPS = ("127.0.0.1", "localhost")
    DEBUG_TOOLBAR_CONFIG = {
        "JQUERY_URL": "",
    }

CSP_REPORT_ONLY = True
CSP_DEFAULT_SRC = ["'self'", "'unsafe-inline'", "'unsafe-eval'", "data:", "blob:", "*"]

if os.getenv("DATABASE") == "postgresql":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "django",
            "USER": "django",
            "PASSWORD": "",
            "HOST": "",
            "PORT": "5555",
            "OPTIONS": {},
        }
    }

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
        "null": {"class": "logging.NullHandler"},
    },
    "loggers": {"": {"handlers": ["console"], "level": "INFO"}},
}

# The local.py import happen at the end of this file so that it can overwrite
# any defaults in dev.py.
# Special cases are:
# 1) ADDITIONAL_APPS in local.py should be appended to INSTALLED_APPS.
# 2) CKEDITOR_URL should be inserted into CKEDITOR_CONFIGS in the correct location.

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

"""
Django settings for test project.

Generated by 'django-admin startproject' using Django 1.8.17.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(PROJECT_DIR))

SECRET_KEY = "not_so_secret_secret_key"
SITE_ID = 1
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"
DEBUG = True

ALLOWED_HOSTS = []

# Applicationdefinition

INSTALLED_APPS = (
    # adhocracy4 base apps
    "adhocracy4.organisations",
    "adhocracy4.projects",
    "adhocracy4.modules",
    "adhocracy4.phases",
    "adhocracy4.reports",
    "adhocracy4.comments",
    "adhocracy4.comments_async",
    "adhocracy4.maps",
    "adhocracy4.actions",
    "adhocracy4.follows",
    "adhocracy4.filters",
    "adhocracy4.forms",
    "adhocracy4.rules",
    "adhocracy4.dashboard",
    "adhocracy4.polls",
    "adhocracy4.administrative_districts",
    "adhocracy4.exports",
    # adhocrayc4 generic apps
    "adhocracy4.ratings",
    "adhocracy4.categories",
    "adhocracy4.labels",
    # adhocracy4 helper apps
    "adhocracy4.ckeditor",
    "adhocracy4.images",
    # test apps
    "tests.apps.questions",
    "tests.apps.locations",
    "tests.apps.ideas",
    "tests.apps.organisations",
    "tests.apps.moderatorfeedback",
    # mandatory third party apps
    "easy_thumbnails",
    "rules.apps.AutodiscoverRulesConfig",
    "background_task",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.sites",
    "django.contrib.staticfiles",
)

MIDDLEWARE = (
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
)

ROOT_URLCONF = "tests.project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(PROJECT_DIR, "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "tests.project.wsgi.application"

# Auth
# https://docs.djangoproject.com/en/1.8/topics/auth/customizing/

AUTHENTICATION_BACKENDS = (
    "rules.permissions.ObjectPermissionBackend",
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
        "TEST": {
            "NAME": os.path.join(BASE_DIR, "test_db.sqlite3"),
        },
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = "/static/"

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"


# Adhcoracy 4

A4_ORGANISATIONS_MODEL = "a4test_organisations.Organisation"
A4_ORGANISATION_FACTORY = "tests.apps.organisations.factories.OrganisationFactory"
A4_RATEABLES = (
    ("a4test_questions", "question"),
    ("a4comments", "comment"),
)
A4_REPORTABLES = (("a4test_questions", "question"),)
A4_COMMENTABLES = (
    ("a4test_questions", "question"),
    ("a4comments", "comment"),
)
A4_ACTIONABLES = ()
A4_AUTO_FOLLOWABLES = (("a4comments", "comment"),)
A4_CATEGORIZABLE = (("a4test_questions", "question"),)
A4_LABELS_ADDABLE = (("a4test_questions", "question"),)
A4_DASHBOARD = {"BLUEPRINTS": "tests.project.blueprints.blueprints"}


# Rich text fields

BLEACH_LIST = {
    "default": {
        "tags": ["p", "strong", "em", "u", "ol", "li", "ul", "a"],
        "attributes": {
            "a": ["href", "rel"],
        },
    },
    "image-editor": {
        "tags": ["p", "strong", "em", "u", "ol", "li", "ul", "a", "img"],
        "attributes": {"a": ["href", "rel"], "img": ["src", "alt", "style"]},
        "styles": [
            "float",
            "margin",
            "padding",
            "width",
            "height",
            "margin-bottom",
            "margin-top",
            "margin-left",
            "margin-right",
        ],
    },
    "collapsible-image-editor": {
        "tags": ["p", "strong", "em", "u", "ol", "li", "ul", "a", "img", "div"],
        "attributes": {
            "a": ["href", "rel"],
            "img": ["src", "alt", "style"],
            "div": ["class"],
        },
        "styles": [
            "float",
            "margin",
            "padding",
            "width",
            "height",
            "margin-bottom",
            "margin-top",
            "margin-left",
            "margin-right",
        ],
    },
}

A4_PROJECT_TOPICS = (
    ("ANT", "Anti-discrimination"),
    ("WOR", "Work & economy"),
    ("BUI", "Building & living"),
)

A4_COMMENT_CATEGORIES = (
    ("QUE", "Question"),
    ("REM", "Remark"),
)

LOGIN_URL = "/accounts/login"

IMAGE_ALIASES = {
    "*": {
        "max_size": 5 * 10**6,
        "fileformats": ("image/png", "image/jpeg", "image/gif"),
    },
    "heroimage": {"min_resolution": (1300, 600)},
    "tileimage": {"min_resolution": (500, 300)},
}

try:
    from .local import *  # noqa: F403, F401
except ImportError:
    pass

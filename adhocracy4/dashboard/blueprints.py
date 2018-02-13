from collections import namedtuple

from django.conf import settings
from django.utils.module_loading import import_string

ProjectBlueprint = namedtuple(
    'ProjectBlueprint', [
        'title', 'description', 'content', 'image', 'settings_model'
    ]
)


def get_blueprints():
    key = 'BLUEPRINTS'
    dashboard_settings = settings.A4_DASHBOARD
    return import_string(dashboard_settings[key])

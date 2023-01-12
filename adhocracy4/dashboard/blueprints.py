from collections import namedtuple

from django.conf import settings
from django.utils.module_loading import import_string

if hasattr(settings, "A4_BLUEPRINT_TYPES"):
    ProjectBlueprint = namedtuple(
        "ProjectBlueprint",
        ["title", "description", "content", "image", "settings_model", "type"],
    )
else:
    ProjectBlueprint = namedtuple(
        "ProjectBlueprint",
        ["title", "description", "content", "image", "settings_model"],
    )


def get_blueprints():
    key = "BLUEPRINTS"
    dashboard_settings = settings.A4_DASHBOARD
    return import_string(dashboard_settings[key])

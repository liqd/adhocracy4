from django.conf import settings
from django.templatetags.static import static

default_app_config = 'adhocracy4.categories.apps.Config'


def has_icons(module):
    if not hasattr(settings, 'A4_CATEGORY_ICONS'):
        return False

    module_settings = module.settings_instance
    return module_settings and hasattr(module_settings, 'polygon')


def get_category_icon_url(name):
    if not name:
        name = 'default'
    return static('category_icons/icons/{}_icon.svg'.format(name))


def get_category_pin_url(name):
    if not name:
        name = 'default'
    return static('category_icons/pins/{}_pin.svg'.format(name))

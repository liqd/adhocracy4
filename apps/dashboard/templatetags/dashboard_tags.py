from django import template

from apps.dashboard.blueprints import blueprints
from apps.dashboard.views import get_management_view
from apps.exports.views import get_exports

register = template.Library()


@register.filter
def has_management_view(project):
    return get_management_view(project) is not None


@register.filter
def get_blueprint_title(key):
    for k, blueprint in blueprints:
        if k == key:
            return blueprint.title
    return key


@register.filter
def has_exports(project):
    return len(get_exports(project)) > 0

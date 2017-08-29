from django import template

from meinberlin.apps.dashboard.blueprints import blueprints
from meinberlin.apps.dashboard.views import get_management_view
from meinberlin.apps.exports import get_exports

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

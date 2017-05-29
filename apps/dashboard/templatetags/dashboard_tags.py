from django import template

from ..blueprints import blueprints
from ..views import get_management_view

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

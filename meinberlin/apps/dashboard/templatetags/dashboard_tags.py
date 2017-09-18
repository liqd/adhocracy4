from django import template

from meinberlin.apps.dashboard2.blueprints import get_blueprints

register = template.Library()


@register.filter
def get_blueprint_title(key):
    for k, blueprint in get_blueprints():
        if k == key:
            return blueprint.title
    return key

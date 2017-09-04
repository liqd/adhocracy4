from django import template

from meinberlin.apps.dashboard2 import blueprints

register = template.Library()


@register.filter
def get_blueprint_title(key):
    for k, blueprint in blueprints.blueprints:
        if k == key:
            return blueprint.title
    return key

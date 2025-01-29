import json

from django import template
from django.utils.html import format_html

from adhocracy4.maps_react.utils import get_map_settings

register = template.Library()


@register.simple_tag()
def react_choose_point(polygon, point, name):
    attributes = {
        "map": get_map_settings(polygon=polygon, point=point, name=name),
    }

    return format_html(
        '<div data-a4-widget="react-choose-point" '
        'data-attributes="{attributes}"></div>',
        attributes=json.dumps(attributes),
    )

from django import template

from adhocracy4 import phases

register = template.Library()


@register.filter
def publish_value_missing(bound_field):
    value = bound_field.value
    if value is True or value is False:
        return False
    return value is None or value == ""


@register.simple_tag
def get_phase_name(type):
    name = phases.content[type].name
    return name


@register.filter
def percentage(value, max_value):
    return round(value / max_value * 100)

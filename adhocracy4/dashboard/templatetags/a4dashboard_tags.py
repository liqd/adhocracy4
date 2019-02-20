from django import template

from adhocracy4 import phases

register = template.Library()


@register.simple_tag
def get_phase_name(type):
    name = phases.content[type].name
    return name


@register.filter
def percentage(value, max_value):
    return round(value / max_value * 100)

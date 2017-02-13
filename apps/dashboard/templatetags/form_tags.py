from django import template

from adhocracy4 import phases

register = template.Library()


@register.assignment_tag
def getPhaseName(type):
    name = phases.content.__getitem__(type).name
    return name

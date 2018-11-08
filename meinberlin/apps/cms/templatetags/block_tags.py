from django import template

register = template.Library()


@register.simple_tag()
def get_identifier(item):
    return id(item)

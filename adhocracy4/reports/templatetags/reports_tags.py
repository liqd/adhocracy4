from django import template

register = template.Library()


@register.filter
def verbose_name(value):
    return value._meta.verbose_name

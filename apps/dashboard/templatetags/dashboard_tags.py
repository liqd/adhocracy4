from django import template

from ..views import get_management_view

register = template.Library()


@register.filter
def has_management_view(project):
    return get_management_view(project) is not None

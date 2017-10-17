from django import template

from adhocracy4.rules.discovery import NormalUser

register = template.Library()


@register.assignment_tag
def would_have_perm(perm, obj=None):
    """
    Check if the NormalUser has the given permission.
    This checks only permissions defined with django-rules.
    """
    return NormalUser().would_have_perm(perm, obj)

from django import template

from adhocracy4.rules.discovery import NormalUser

register = template.Library()


@register.simple_tag
def would_have_perm(perm, obj=None):
    """
    Check if the NormalUser has the given permission.
    This checks only permissions defined with django-rules.
    """
    return NormalUser().would_have_perm(perm, obj)


@register.simple_tag
def has_or_would_have_perm(perm, user, obj=None):
    """
    Check if the NormalUser has the given permission.
    This checks only permissions defined with django-rules.
    """
    if not hasattr(user, 'has_perm'):  # pragma: no cover
        return False  # swapped user model that doesn't support permissions
    elif user.is_authenticated:
        return user.has_perm(perm, obj)
    else:
        return NormalUser().would_have_perm(perm, obj)

from django import template

register = template.Library()


@register.assignment_tag
def filter_has_perm(perm, user, objects):
    if not hasattr(user, 'has_perm'):  # pragma: no cover
        return objects  # swapped user model that doesn't support permissions
    else:
        return (obj for obj in objects if user.has_perm(perm, obj))

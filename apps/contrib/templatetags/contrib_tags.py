from django import template
from django.template.loader import render_to_string

register = template.Library()


@register.assignment_tag
def include_template_string(template, **kwargs):
    rendered_template = render_to_string(template, kwargs)
    return str(rendered_template)


@register.assignment_tag
def combined_url_parameter(request_query_dict, **kwargs):
    combined_query_dict = request_query_dict.copy()
    for key in kwargs:
        combined_query_dict.setlist(key, [kwargs[key]])
    encoded_parameter = '?' + combined_query_dict.urlencode()
    return encoded_parameter


@register.assignment_tag
def filter_has_perm(perm, user, objects):
    """Filter a list of objects based on user permissions."""
    if not hasattr(user, 'has_perm'):
        # If the swapped user model does not support permissions, all objects
        # will be returned. This is taken from rules.templatetags.has_perm.
        return objects
    else:
        return [obj for obj in objects if user.has_perm(perm, obj)]

from django import template
from django.template.loader import render_to_string

register = template.Library()


@register.assignment_tag
def includeTemplateString(template, **kwargs):
    rendered_template = render_to_string(template, kwargs)
    return str(rendered_template)


@register.assignment_tag
def combinedUrlParameter(request_query_dict, **kwargs):
    combined_query_dict = request_query_dict.copy()
    for key in kwargs:
        combined_query_dict.setlist(key, [kwargs[key]])
    encoded_parameter = '?' + combined_query_dict.urlencode()
    return encoded_parameter


@register.assignment_tag
def get_item_view_permission(item):
    return get_item_permission(item, 'view')


@register.assignment_tag
def get_item_add_permission(item):
    return get_item_permission(item, 'add')


@register.assignment_tag
def get_item_change_permission(item):
    return get_item_permission(item, 'change')


@register.assignment_tag
def get_item_delete_permission(item):
    return get_item_permission(item, 'delete')


def get_item_permission(item, verb):
    return '{app}.{verb}_{name}'.format(
        app=item._meta.app_label,
        verb=verb,
        name=item._meta.verbose_name
    )

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

from django import template
from django.template.loader import render_to_string

register = template.Library()


@register.assignment_tag
def includeTemplateString(template, **kwargs):
    rendered_template = render_to_string(template, kwargs)
    return str(rendered_template)

from django import template
from django.utils.html import format_html

register = template.Library()


@register.simple_tag
def react_polls():
    return format_html(
        (
            '<div id="{id}"></div>'
            '<script>window.adhocracy4.renderPolls("{id}")</script>'
        ),
        id='TODO'
    )

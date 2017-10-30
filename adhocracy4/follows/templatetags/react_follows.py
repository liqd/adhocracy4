from django import template
from django.utils.html import format_html

register = template.Library()


@register.simple_tag()
def react_follows(project):
    return format_html(
        '<span data-a4-widget="follows" data-project={project}></span>',
        project=project.slug
    )

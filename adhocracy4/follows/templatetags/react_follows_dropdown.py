from django import template
from django.utils.html import format_html

register = template.Library()


@register.simple_tag()
def react_follows_dropdown(project):
    return format_html(
        '<span data-a4-widget="follows_dropdown" data-project={project}>'
        '</span>',
        project=project.slug
    )

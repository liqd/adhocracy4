from django import template
from django.utils.html import format_html

register = template.Library()


@register.simple_tag()
def react_follows(project):
    mountpoint = 'follows_for_project_{pk}'.format(pk=project.pk)

    return format_html(
        (
            '<span id="{mountpoint}" data-project={project}></span>'
            "<script>window.adhocracy4.renderFollow('{mountpoint}')</script>"
        ),
        project=project.slug,
        mountpoint=mountpoint
    )

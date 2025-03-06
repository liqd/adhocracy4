import json

from django import template
from django.utils.html import format_html

register = template.Library()


@register.simple_tag(takes_context=True)
def react_follows(context, project, alert_target=None, custom_classes=""):
    request = context["request"]
    user = request.user
    authenticated_as = None
    if user.is_authenticated:
        authenticated_as = user.username

    attributes = {"project": project.slug, "authenticatedAs": authenticated_as}

    if custom_classes:
        attributes["customClasses"] = custom_classes
    if alert_target:
        attributes["alertTarget"] = alert_target

    return format_html(
        '<span data-a4-widget="follows" data-attributes="{attributes}"></span>',
        attributes=json.dumps(attributes),
    )

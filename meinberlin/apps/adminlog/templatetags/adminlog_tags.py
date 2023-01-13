from django import template

from meinberlin.apps.adminlog import models

register = template.Library()


@register.simple_tag()
def logentry_icon_class(logentry):
    if logentry.action == models.PROJECT_COMPONENT_UPDATED:
        return "fas fa-pencil-alt"
    elif logentry.action == models.MODULE_COMPONENT_UPDATED:
        return "fas fa-pencil-alt"
    elif logentry.action == models.PROJECT_CREATED:
        return "fas fa-check"
    elif logentry.action == models.PROJECT_PUBLISHED:
        return "fas fa-play"
    elif logentry.action == models.PROJECT_UNPUBLISHED:
        return "fas fa-stop"
    elif logentry.action == models.MODULE_CREATED:
        return "fas fa-check"
    elif logentry.action == models.MODULE_PUBLISHED:
        return "fas fa-plus"
    elif logentry.action == models.MODULE_UNPUBLISHED:
        return "fas fa-minus"

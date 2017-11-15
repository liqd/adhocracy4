from django import template

from meinberlin.apps.adminlog import models

register = template.Library()


@register.simple_tag()
def logentry_icon(logentry):
    if logentry.action == models.PROJECT_COMPONENT_UPDATED:
        return 'pencil'
    elif logentry.action == models.MODULE_COMPONENT_UPDATED:
        return 'pencil'
    elif logentry.action == models.PROJECT_CREATED:
        return 'plus'
    elif logentry.action == models.PROJECT_PUBLISHED:
        return 'play'
    elif logentry.action == models.PROJECT_UNPUBLISHED:
        return 'stop'

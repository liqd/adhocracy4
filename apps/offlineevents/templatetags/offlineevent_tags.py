from django import template

from adhocracy4.modules.models import Module
from adhocracy4.phases.models import Phase
from apps.offlineevents.models import OfflineEvent

register = template.Library()


@register.assignment_tag
def offlineevents_and_modules_sorted(project):
    modules = list(project.module_set.all())
    events = list(OfflineEvent.objects.filter(project=project))
    res = modules + events
    res_sorted = sorted(
        res, key=lambda x: x.first_phase_start_date if
        isinstance(x, Module) else x.date)
    return res_sorted


@register.filter
def is_phase(obj):
    return isinstance(obj, Phase)


@register.filter
def is_module(obj):
    return isinstance(obj, Module)


@register.filter
def is_offlineevent(obj):
    return isinstance(obj, OfflineEvent)

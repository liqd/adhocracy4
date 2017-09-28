from functools import cmp_to_key

from django import template

from adhocracy4.modules.models import Module
from adhocracy4.phases.models import Phase
from meinberlin.apps.offlineevents.models import OfflineEvent

register = template.Library()


@register.assignment_tag
def offlineevents_and_modules_sorted(project):
    modules = list(project.module_set.all())
    events = list(OfflineEvent.objects.filter(project=project))
    res = modules + events
    return sorted(res, key=cmp_to_key(_cmp))


def _cmp(x, y):
    x = x.first_phase_start_date if isinstance(x, Module) else x.date
    if x is None:
        return 1

    y = y.first_phase_start_date if isinstance(y, Module) else y.date
    if y is None:
        return -1

    return (x > y) - (y < x)


@register.filter
def is_phase(obj):
    return isinstance(obj, Phase)


@register.filter
def is_module(obj):
    return isinstance(obj, Module)


@register.filter
def is_offlineevent(obj):
    return isinstance(obj, OfflineEvent)

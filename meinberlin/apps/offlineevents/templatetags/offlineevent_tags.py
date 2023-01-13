from functools import cmp_to_key

from django import template

from adhocracy4.modules.models import Module
from adhocracy4.phases.models import Phase
from meinberlin.apps.activities.models import Activity
from meinberlin.apps.offlineevents.models import OfflineEvent

register = template.Library()


@register.simple_tag
def offlineevents_and_modules_sorted(project):
    modules = list(project.module_set.all())
    events = list(OfflineEvent.objects.filter(project=project))
    res = modules + events
    return sorted(res, key=cmp_to_key(_cmp))


def _cmp(x, y):
    x_date = x.first_phase_start_date if isinstance(x, Module) else x.date
    if x_date is None:
        return 1

    y_date = y.first_phase_start_date if isinstance(y, Module) else y.date
    if y_date is None:
        return -1

    if x_date > y_date:
        return 1
    elif x_date == y_date:
        return 0
    else:
        return -1


@register.filter
def is_phase(obj):
    return isinstance(obj, Phase)


@register.filter
def is_module(obj):
    return isinstance(obj, Module)


@register.filter
def is_offlineevent(obj):
    return isinstance(obj, OfflineEvent)


@register.filter
def has_activity(obj):
    try:
        return isinstance(obj.item_set.first().activity, Activity)
    except AttributeError:
        try:
            return isinstance(
                obj.future_phases.first().module.item_set.first().activity, Activity
            )
        except AttributeError:
            return isinstance(obj, Activity)

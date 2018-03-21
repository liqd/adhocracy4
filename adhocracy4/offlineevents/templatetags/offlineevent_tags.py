from django import template

from adhocracy4.modules.models import Module
from adhocracy4.phases.models import Phase
from adhocracy4.offlineevents.models import OfflineEvent

register = template.Library()


@register.filter
def is_phase(obj):
    return isinstance(obj, Phase)


@register.filter
def is_module(obj):
    return isinstance(obj, Module)


@register.filter
def is_offlineevent(obj):
    return isinstance(obj, OfflineEvent)

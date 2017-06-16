from django import template

from adhocracy4.phases.models import Phase
from apps.offlineevents.models import OfflineEvent

register = template.Library()


@register.assignment_tag
def phases_and_offlineevents_sorted(project):
    phases = list(project.phases)
    events = list(OfflineEvent.objects.filter(project=project))
    res = phases + events
    res_sorted = sorted(
        res, key=lambda x: x.start_date if isinstance(x, Phase) else x.date)
    return res_sorted


@register.filter
def is_phase(obj):
    return isinstance(obj, Phase)


@register.filter
def is_offlineevent(obj):
    return isinstance(obj, OfflineEvent)

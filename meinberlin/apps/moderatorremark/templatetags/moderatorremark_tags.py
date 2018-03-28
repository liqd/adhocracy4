from django import template
from rest_framework.renderers import JSONRenderer

from meinberlin.apps.moderatorremark.serializers import \
    ModeratorRemarkSerializer

register = template.Library()


@register.inclusion_tag('meinberlin_moderatorremark/includes/'
                        'popover_remark.html')
def popover_remark(remark):
    context = {
        'remark': remark
    }

    if remark:
        serializer = ModeratorRemarkSerializer(remark)
        remark_json = JSONRenderer().render(serializer.data)
        context['attributes'] = remark_json

    return context

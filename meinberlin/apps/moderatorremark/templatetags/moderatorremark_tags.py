from django import template
from django.contrib.contenttypes.models import ContentType
from rest_framework.renderers import JSONRenderer

from meinberlin.apps.moderatorremark.models import ModeratorRemark
from meinberlin.apps.moderatorremark.serializers import ModeratorRemarkSerializer

register = template.Library()


@register.inclusion_tag("meinberlin_moderatorremark/includes/" "popover_remark.html")
def popover_remark(item):
    remark = getattr(item, "remark", None)

    context = {"remark": remark, "object": item}

    if remark:
        serializer = ModeratorRemarkSerializer(remark)
        remark_json = JSONRenderer().render(serializer.data).decode("utf-8")
        context["attributes"] = remark_json
    else:
        content_type = ContentType.objects.get_for_model(item)
        empty_remark = ModeratorRemark(
            item_content_type=content_type, item_object_id=item.id
        )
        serializer = ModeratorRemarkSerializer(empty_remark)
        remark_json = JSONRenderer().render(serializer.data).decode("utf-8")
        context["attributes"] = remark_json

    return context

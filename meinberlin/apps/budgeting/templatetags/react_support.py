import json

from django import template
from django.contrib.contenttypes.models import ContentType
from django.utils.html import format_html

from adhocracy4.ratings import models as rating_models

register = template.Library()


@register.simple_tag(takes_context=True)
def react_support(context, obj):
    request = context['request']
    user = request.user

    contenttype = ContentType.objects.get_for_model(obj)
    authenticated = False
    user_supported = False
    user_support_id = -1
    if user.is_authenticated:
        authenticated = True
        user_support = rating_models.Rating.objects.filter(
            content_type=contenttype,
            object_pk=obj.pk,
            creator=user.pk
        ).first()
        if user_support:
            user_supported = bool(user_support.value)
            user_support_id = user_support.pk

    attributes = {
        'contentType': contenttype.pk,
        'objectId': obj.pk,
        'authenticated': authenticated,
        'support': obj.positive_rating_count,
        'userSupported': user_supported,
        'userSupportId': user_support_id,
        'style': 'ideas',
    }

    return format_html(
        '<div data-mb-widget="support" data-attributes="{attributes}"></div>',
        attributes=json.dumps(attributes)
    )

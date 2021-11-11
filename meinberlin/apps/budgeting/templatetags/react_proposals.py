import json

from django import template
from django.urls import reverse
from django.utils.html import format_html

# from django.urls import reverse
# from django.utils.translation import gettext_lazy as _
# from adhocracy4.rules.discovery import NormalUser

register = template.Library()


@register.simple_tag(takes_context=True)
def react_proposals(context, obj):
    proposals_api_url = reverse('proposals-list', kwargs={'module_pk': obj.pk})
    attributes = {'proposals_api_url': proposals_api_url}

    return format_html(
        '<div data-mb-widget="proposals" '
        'data-attributes="{attributes}"></div>',
        attributes=json.dumps(attributes)
    )

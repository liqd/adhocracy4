import json

from django import template
from django.urls import reverse
from django.utils.html import format_html

register = template.Library()


@register.simple_tag(takes_context=True)
def react_proposals(context, obj):
    proposals_api_url = reverse('proposals-list', kwargs={'module_pk': obj.pk})
    attributes = {'proposals_api_url': proposals_api_url,
                  'is_voting_phase': 'voting' in obj.active_phase.type}

    return format_html(
        '<div data-mb-widget="proposals" '
        'data-attributes="{attributes}"></div>',
        attributes=json.dumps(attributes)
    )

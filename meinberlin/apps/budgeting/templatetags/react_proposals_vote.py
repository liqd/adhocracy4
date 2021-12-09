import json

from django import template
from django.urls import reverse
from django.utils.html import format_html

from adhocracy4.phases.predicates import has_feature_active
from meinberlin.apps.budgeting.models import Proposal

register = template.Library()


@register.simple_tag(takes_context=True)
def react_proposals_vote(context, module):
    proposals_api_url = reverse('proposals-list',
                                kwargs={'module_pk': module.pk})
    attributes = {'proposals_api_url': proposals_api_url,
                  'is_voting_phase': has_feature_active(module,
                                                        Proposal,
                                                        'vote')
                  }
    return format_html(
        '<div data-mb-widget="vote_button" '
        'data-attributes="{attributes}"></div>',
        attributes=json.dumps(attributes)
    )

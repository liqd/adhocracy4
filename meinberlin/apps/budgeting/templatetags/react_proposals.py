import json

from django import template
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.utils.html import format_html

from adhocracy4.phases.predicates import has_feature_active
from meinberlin.apps.budgeting.models import Proposal

register = template.Library()


@register.simple_tag(takes_context=True)
def react_proposals(context, module):
    proposals_api_url = reverse('proposals-list',
                                kwargs={'module_pk': module.pk})
    proposal_ct = ContentType.objects.get(app_label='meinberlin_budgeting',
                                          model='proposal')
    tokenvote_api_url = reverse('tokenvotes-list',
                                kwargs={'content_type': proposal_ct.id})

    attributes = {'proposals_api_url': proposals_api_url,
                  'tokenvote_api_url': tokenvote_api_url,
                  'is_voting_phase': has_feature_active(module,
                                                        Proposal,
                                                        'vote')
                  }

    return format_html(
        '<div data-mb-widget="proposals" '
        'data-attributes="{attributes}"></div>',
        attributes=json.dumps(attributes)
    )

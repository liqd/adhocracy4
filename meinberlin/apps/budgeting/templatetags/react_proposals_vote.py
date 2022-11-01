import json

from django import template
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.utils.html import format_html

from meinberlin.apps.votes.models import TokenVote
from meinberlin.apps.votes.models import VotingToken
from meinberlin.apps.votes.serializers import VotingTokenSerializer

register = template.Library()


@register.simple_tag(takes_context=True)
def react_proposals_vote(context, module, proposal):
    proposal_ct = ContentType.objects.get(app_label='meinberlin_budgeting',
                                          model='proposal')
    tokenvote_api_url = reverse('tokenvotes-list',
                                kwargs={
                                    'module_pk': module.pk,
                                    'content_type': proposal_ct.id
                                })

    request = context['request']
    session_token_voted = False
    token_info = None
    if 'voting_token' in request.session:
        try:
            token = VotingToken.objects.get(
                token=request.session['voting_token'],
                module=module
            )
            serializer = VotingTokenSerializer(token)
            token_info = serializer.data
            session_token_voted = TokenVote.objects.filter(
                token__pk=token.pk,
                content_type=proposal_ct,
                object_pk=proposal.pk
            ).exists()
        except VotingToken.DoesNotExist:
            pass

    attributes = {'tokenvote_api_url': tokenvote_api_url,
                  'objectID': proposal.pk,
                  'session_token_voted': session_token_voted,
                  'token_info': token_info
                  }

    return format_html(
        '<div data-mb-widget="vote_button" '
        'data-attributes="{attributes}"></div>',
        attributes=json.dumps(attributes)
    )

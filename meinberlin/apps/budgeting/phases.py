from django.utils.translation import ugettext_lazy as _

from adhocracy4 import phases

from . import apps
from . import models
from . import views


class RequestPhase(phases.PhaseContent):
    app = apps.Config.label
    phase = 'submit'
    view = views.ProposalListView

    name = _('Request phase')
    description = _('Participants can submit proposals, comment on and '
                    'rate them.')
    module_name = _('participatory budgeting')

    features = {
        'crud': (models.Proposal,),
        'comment': (models.Proposal,),
        'rate': (models.Proposal,),
    }


class CollectPhase(phases.PhaseContent):
    app = apps.Config.label
    phase = 'collect'
    view = views.ProposalListView

    name = _('Proposal phase')
    description = _('Participants can submit proposals and comment on them.')
    module_name = _('participatory budgeting 2 phases')

    features = {
        'crud': (models.Proposal,),
        'comment': (models.Proposal,),
    }


class RatingPhase(phases.PhaseContent):
    app = apps.Config.label
    phase = 'rating'
    view = views.ProposalListView

    name = _('Rating phase')
    description = _('Participants can vote on the proposals.')
    module_name = _('participatory budgeting 2 phases')

    features = {
        'rate': (models.Proposal,)
    }


phases.content.register(RequestPhase())
phases.content.register(CollectPhase())
phases.content.register(RatingPhase())

from django.utils.translation import gettext_lazy as _

from adhocracy4 import phases

from . import apps
from . import models
from . import views


class RequestPhase(phases.PhaseContent):
    app = apps.Config.label
    phase = 'submit'
    view = views.ProposalListView

    name = _('What ideas do you suggest for funding?')
    description = _('You can enter your proposal on the map and comment on '
                    'and rate the proposals of the other participants.')
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

    name = _('What ideas do you suggest for funding?')
    description = _('You can enter your proposal on the map and comment on '
                    'the proposals of the other participants.')
    module_name = _('participatory budgeting 2 phases')

    features = {
        'crud': (models.Proposal,),
        'comment': (models.Proposal,),
    }


class RatingPhase(phases.PhaseContent):
    app = apps.Config.label
    phase = 'rating'
    view = views.ProposalListView

    name = _('How do you like the submitted proposals?')
    description = _('Rate the submitted proposals for the participatory '
                    'budget (for/against).')
    module_name = _('participatory budgeting 2 phases')

    features = {
        'rate': (models.Proposal,)
    }


class VotingPhase(phases.PhaseContent):
    app = apps.Config.label
    phase = 'voting'
    view = views.ProposalListView

    name = _('Which of the proposals do you think should be implemented?')
    description = _('You can vote for up to 5 proposals. '
                    'To do so, please enter the voting code.')
    module_name = _('participatory budgeting 3 phases')

    features = {
        'vote': (models.Proposal,)
    }


phases.content.register(RequestPhase())
phases.content.register(CollectPhase())
phases.content.register(RatingPhase())
phases.content.register(VotingPhase())

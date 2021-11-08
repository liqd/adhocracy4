from django.utils.translation import gettext_lazy as _

from adhocracy4 import phases

from . import apps
from . import models
from . import views


class RequestPhase(phases.PhaseContent):
    app = apps.Config.label
    phase = 'submit'
    view = views.ProposalListView

    name = _('Request phase')
    description = _('Request budgeting.')
    module_name = _('kiezkasse')

    features = {
        'crud': (models.Proposal,),
        'comment': (models.Proposal,),
    }


class FeedbackPhase(phases.PhaseContent):
    app = apps.Config.label
    phase = 'feedback'
    view = views.ProposalListView

    name = _('Feedback phase')
    description = _('Get feedback for budgeting requests through rates and '
                    'comments.')
    module_name = _('kiezkasse')

    features = {
        'rate': (models.Proposal,),
        'comment': (models.Proposal,)
    }


class RequestFeedbackPhase(phases.PhaseContent):
    app = apps.Config.label
    phase = 'request_feedback'
    view = views.ProposalListView

    name = _('What ideas do you suggest for funding?')
    description = _('You can enter your proposal on the map and comment on '
                    'and rate the proposals of the other participants.')
    module_name = _('kiezkasse')

    features = {
        'crud': (models.Proposal,),
        'rate': (models.Proposal,),
        'comment': (models.Proposal,)
    }


phases.content.register(RequestPhase())
phases.content.register(FeedbackPhase())
phases.content.register(RequestFeedbackPhase())

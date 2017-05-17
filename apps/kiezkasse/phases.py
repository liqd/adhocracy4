from django.utils.translation import ugettext_lazy as _

from adhocracy4 import phases

from . import apps
from . import models
from . import views


class RequestPhase(phases.PhaseContent):
    app = apps.Config.label
    phase = 'submit'
    weight = 20
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
    weight = 40
    view = views.ProposalListView

    name = _('Feedback phase')
    description = _('Get feedback for budgeting requests through rates and '
                    'comments.')
    module_name = _('kiezkasse')

    features = {
        'rate': (models.Proposal,),
        'comment': (models.Proposal,)
    }


phases.content.register(RequestPhase())
phases.content.register(FeedbackPhase())

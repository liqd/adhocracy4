from django.utils.translation import ugettext_lazy as _

from adhocracy4 import phases

from . import apps
from . import models
from . import views


class CreatePollPhase(phases.PhaseContent):
    app = apps.Config.label
    phase = 'create'
    weight = 10
    view = views.PollCreateView

    name = _('Create poll phase')
    module_name = _('polls')
    description = _('Create questions and choices for the poll.')

    features = {}


class VotingPhase(phases.PhaseContent):
    app = apps.Config.label
    phase = 'voting'
    weight = 20
    view = views.PollDetailView

    name = _('Voting phase')
    description = _('Cast votes and discuss the poll.')
    module_name = _('polls')

    features = {
        'crud': (models.Vote,),
        'comment': (models.Poll,),
    }


class CommentPhase(phases.PhaseContent):
    app = apps.Config.label
    phase = 'voting'
    weight = 30
    view = views.PollDetailView

    name = _('Comment phase')
    description = _('Discuss the poll results.')
    module_name = _('polls')

    features = {
        'comment': (models.Poll,),
    }

phases.content.register(CreatePollPhase())
phases.content.register(VotingPhase())
phases.content.register(CommentPhase())

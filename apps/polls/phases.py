from django.utils.translation import ugettext_lazy as _

from adhocracy4 import phases

from . import apps
from . import models
from . import views


class VotingPhase(phases.PhaseContent):
    app = apps.Config.label
    phase = 'voting'
    weight = 20
    view = views.PollDetailView
    management_view = views.PollManagementView

    name = _('Voting phase')
    description = _('Cast votes and discuss the poll.')
    module_name = _('polls')

    features = {
        'crud': (models.Vote,),
        'comment': (models.Poll,),
    }

phases.content.register(VotingPhase())

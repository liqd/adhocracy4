from django.utils.translation import ugettext_lazy as _

from adhocracy4 import phases

from . import apps
from . import models
from . import views


class VotingPhase(phases.PhaseContent):
    app = apps.Config.label
    phase = 'voting'
    view = views.PollDetailView

    name = _('Please take part in our poll!')
    description = _('Help us by answering the questions below. There is '
                    'space for your comments at the end of the questionnaire.')
    module_name = _('polls')

    features = {
        'crud': (models.Vote,),
        'comment': (models.Poll,),
    }


phases.content.register(VotingPhase())

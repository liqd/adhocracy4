from django.utils.translation import pgettext_lazy
from django.utils.translation import ugettext_lazy as _

from adhocracy4 import phases

from . import apps
from . import models
from . import views


class VotingPhase(phases.PhaseContent):
    app = apps.Config.label
    phase = 'voting'
    view = views.PollDetailView

    name = pgettext_lazy('A4: voting phase name', 'Voting phase')
    description = pgettext_lazy(
        'A4: voting phase description',
        'Answer the questions and comment on the poll.'
    )
    module_name = _('polls')

    features = {
        'crud': (models.Vote,),
        'comment': (models.Poll,),
    }


phases.content.register(VotingPhase())

from django.utils.translation import gettext_lazy as _
from django.utils.translation import pgettext_lazy

from adhocracy4 import phases

from . import apps
from . import models
from . import views


class VotingPhase(phases.PhaseContent):
    app = apps.Config.label
    phase = "voting"
    view = views.OpenPollDetailView

    name = pgettext_lazy("A4: voting phase name", "Voting phase")
    description = pgettext_lazy(
        "A4: voting phase description", "Answer the questions and comment on the poll."
    )
    module_name = _("open polls")

    features = {
        "crud": (models.Vote,),
        "comment": (models.OpenPoll,),
    }


phases.content.register(VotingPhase())

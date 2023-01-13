from django.utils.translation import gettext_lazy as _

from adhocracy4 import phases

from . import apps
from . import models
from . import views


class PrioritizePhase(phases.PhaseContent):
    app = apps.Config.label
    phase = "prioritize"
    view = views.TopicListView

    name = _("What do you think about these ideas/topics?")
    description = _("You can comment on and rate the ideas/topics.")
    module_name = _("topic prioritization")

    features = {
        "comment": (models.Topic,),
        "rate": (models.Topic,),
    }


phases.content.register(PrioritizePhase())

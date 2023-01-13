from django.utils.translation import gettext_lazy as _

from adhocracy4 import phases

from . import apps
from . import models
from . import views


class PrioritizePhase(phases.PhaseContent):
    app = apps.Config.label
    phase = "prioritize"
    view = views.MapTopicListView

    name = _("What do you think about these places/suggestions?")
    description = _("You can comment and rate the places/suggestions.")
    module_name = _("place prioritization")

    features = {
        "comment": (models.MapTopic,),
        "rate": (models.MapTopic,),
    }


phases.content.register(PrioritizePhase())

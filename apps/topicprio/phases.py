from django.utils.translation import ugettext_lazy as _

from adhocracy4 import phases

from . import apps
from . import models
from . import views


class CreatePhase(phases.PhaseContent):
    app = apps.Config.label
    phase = 'create'
    weight = 10
    view = views.TopicCreateListView

    name = _('Create phase')
    description = _('Moderators create topics.')
    module_name = _('topic prioritization')

    features = {
        'crud': (models.Topic,),
    }


class PrioritizePhase(phases.PhaseContent):
    app = apps.Config.label
    phase = 'prioritize'
    weight = 20
    view = views.TopicListView

    name = _('Collect phase')
    description = _('Prioritize and comment topics.')
    module_name = _('topic prioritization')

    features = {
        'comment': (models.Topic,),
        'rate': (models.Topic,),
    }

phases.content.register(CreatePhase())
phases.content.register(PrioritizePhase())

from adhocracy4 import phases

from . import apps
from . import models
from . import views


class AskPhase(phases.PhaseContent):
    app = apps.Config.label
    phase = 'ask'
    view = views.QuestionList

    name = 'Asking Phase'
    description = 'Ask questions'
    module_name = 'test questions'

    features = {
        'crud': (models.Question, ),
        'comment': (models.Question, )
    }


phases.content.register(AskPhase())


class RatePhase(phases.PhaseContent):
    app = apps.Config.label
    phase = 'rate'
    view = views.QuestionList

    name = 'Rating Phase'
    description = 'Rate questions'
    module_name = 'test questions'

    features = {
        'rate': (models.Question, ),
    }


phases.content.register(RatePhase())

from adhocracy4 import phases

from . import apps, models, views


class AskPhase(phases.PhaseContent):
    app = apps.QuestionsConfig.label
    phase = 'ask'
    view = views.QuestionList

    name = 'Asking Phase'
    description = 'Ask questions'

    features = {
         'crud': (models.Question, ),
         'comment': (models.Question, )
    }


phases.content.register(AskPhase())


class RatePhase(phases.PhaseContent):
    app = apps.QuestionsConfig.label
    phase = 'rate'
    view = views.QuestionList

    name = 'Rating Phase'
    description = 'Rate questions'

    features = {
         'rate': (models.Question, ),
    }


phases.content.register(RatePhase())

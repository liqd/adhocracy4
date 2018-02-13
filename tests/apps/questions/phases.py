from adhocracy4 import phases

from . import apps, models, views


class AskPhase(phases.PhaseContent):
    app = apps.QuestionsConfig.label
    phase = 'ask'
    weight = 10
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
    app = apps.QuestionsConfig.label
    phase = 'rate'
    weight = 20
    view = views.QuestionList

    name = 'Rating Phase'
    description = 'Rate questions'
    module_name = 'test questions'

    features = {
         'rate': (models.Question, ),
    }


phases.content.register(RatePhase())

from adhocracy4 import phases

from . import apps, models, views


class AskPhase(phases.PhaseContent):
    app = apps.QuestionsConfig.label
    phase = 'ask'
    view = views.QuestionList
    weight = 20

    features = {
         'crud': (models.Question, ),
         'comment': (models.Question, )
    }

phases.content.register(AskPhase())


class RatePhase(phases.PhaseContent):
    app = apps.QuestionsConfig.label
    phase = 'ask'
    view = views.QuestionList
    weight = 30

    features = {
         'rate': (models.Question, ),
    }

phases.content.register(RatePhase())

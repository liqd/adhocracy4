from adhocracy4 import phases

from . import apps, models, views


class AskPhase(phases.PhaseContent):
    app = apps.QuestionsConfig.label
    phase = 'ask'
    view = views.QuestionList
    weight = 20

    features = {
         'crud': (models.Question, )
    }


phases.content.register(AskPhase())

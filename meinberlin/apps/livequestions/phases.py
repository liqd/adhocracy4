from django.utils.translation import ugettext_lazy as _

from adhocracy4 import phases

from . import apps
from . import models
from . import views


class IssuePhase(phases.PhaseContent):
    app = apps.Config.label
    phase = 'issue'
    view = views.LiveQuestionModuleDetail

    name = _('Issue phase')
    description = _('Add questions and support.')
    module_name = _('Interactive Event')
    icon = 'lightbulb-o'

    features = {
        'crud': (models.LiveQuestion,),
        'like': (models.LiveQuestion,)
    }


phases.content.register(IssuePhase())

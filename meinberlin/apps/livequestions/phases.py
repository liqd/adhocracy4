from django.utils.translation import gettext_lazy as _

from adhocracy4 import phases

from . import apps
from . import models
from . import views


class IssuePhase(phases.PhaseContent):
    app = apps.Config.label
    phase = 'issue'
    view = views.LiveQuestionModuleDetail

    name = _('Do you have questions?')
    description = _('You can add your questions and support the questions of '
                    'other participants. To allow different people to have '
                    'their say, please indicate which group you feel you '
                    'belong to.')
    module_name = _('Interactive Event')
    icon = 'lightbulb-o'

    features = {
        'crud': (models.LiveQuestion,),
        'like': (models.LiveQuestion,)
    }


phases.content.register(IssuePhase())

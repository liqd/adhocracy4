from django.utils.translation import ugettext_lazy as _

from adhocracy4 import phases

from . import apps
from . import models
from . import views


class StatementPhase(phases.PhaseContent):
    app = apps.Config.label
    phase = 'statement'
    view = views.BplanStatementFormView

    name = _('Statement phase')
    description = _('Send statement to the office workers per mail.')
    module_name = _('bplan')

    features = {
        'crud': (models.Statement,),
    }


phases.content.register(StatementPhase())

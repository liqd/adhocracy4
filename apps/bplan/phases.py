from django.utils.translation import ugettext_lazy as _

from adhocracy4 import phases

from . import apps
from . import views


class StatementPhase(phases.PhaseContent):
    app = apps.Config.label
    phase = 'statement'
    weight = 10
    view = views.BplanStatementFormView

    name = _('Statement phase')
    description = _('Send statement to the office workers per mail.')
    module_name = _('bplan')

    features = {}


phases.content.register(StatementPhase())

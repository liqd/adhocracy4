from django.utils.translation import ugettext_lazy as _

from adhocracy4 import phases

from . import apps
from . import views


class ExternalPhase(phases.PhaseContent):
    app = apps.Config.label
    phase = 'external'
    weight = 10
    view = views.ExternalProjectRedirectView

    name = _('External phase')
    description = _('External phase.')
    module_name = _('external project')

    features = {}


phases.content.register(ExternalPhase())

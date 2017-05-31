from django.utils.translation import ugettext_lazy as _

from adhocracy4 import phases

from . import apps
from . import models
from . import views


class RequestPhase(phases.PhaseContent):
    app = apps.Config.label
    phase = 'submit'
    weight = 20
    view = views.ProposalListView

    name = _('Request phase')
    description = _('Request budgeting and get feedback through rates and '
                    'comments.')
    module_name = _('participatory budgeting')

    features = {
        'crud': (models.Proposal,),
        'comment': (models.Proposal,),
        'rate': (models.Proposal,),
    }


phases.content.register(RequestPhase())

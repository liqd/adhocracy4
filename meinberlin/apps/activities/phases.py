from django.utils.translation import ugettext_lazy as _

from adhocracy4 import phases

from . import apps
from . import views


class FaceToFacePhase(phases.PhaseContent):
    app = apps.Config.label
    phase = 'facetoface'
    view = views.ActivityView

    name = _('Face to face phase')
    description = _('Take part in face to face participation')
    module_name = _('facetoface')

    features = {}


phases.content.register(FaceToFacePhase())

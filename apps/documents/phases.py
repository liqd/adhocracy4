from django.utils.translation import ugettext_lazy as _

from adhocracy4 import phases

from . import apps
from . import models
from . import views


class CreateDocumentPhase(phases.PhaseContent):
    app = apps.Config.label
    phase = 'create_document'
    view = views.DocumentCreateView
    weight = 30

    name = _('Create document phase')
    module_name = _('commenting text')
    description = _('Create text for the project.')

    features = {}


phases.content.register(CreateDocumentPhase())


class CommentPhase(phases.PhaseContent):
    app = apps.Config.label
    phase = 'comment'
    view = views.DocumentDetailView
    weight = 40

    name = _('Comment phase')
    module_name = _('commenting text')
    description = _('Collect comments for the text.')

    features = {
        'comment': (models.Paragraph, models.Document),
    }


phases.content.register(CommentPhase())

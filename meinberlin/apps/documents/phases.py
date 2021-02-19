from django.utils.translation import ugettext_lazy as _

from adhocracy4 import phases

from . import apps
from . import models
from . import views


class CommentPhase(phases.PhaseContent):
    app = apps.Config.label
    phase = 'comment'
    view = views.DocumentDetailView

    name = _('What do you think about the draft?')
    module_name = _('commenting text')
    description = _('You can comment on the draft paragraph by paragraph or '
                    'as a whole.')

    features = {
        'comment': (models.Paragraph, models.Chapter),
    }


phases.content.register(CommentPhase())

from django.utils.translation import ugettext_lazy as _

from adhocracy4 import phases

from . import apps
from . import models
from . import views


class IssuePhase(phases.PhaseContent):
    app = apps.Config.label
    phase = 'issue'
    view = views.MapIdeaListView

    name = _('Issue phase')
    description = _('Create new ideas located on a map.')
    module_name = _('ideas collection')

    features = {
        'crud': (models.MapIdea,),
    }


class CollectPhase(phases.PhaseContent):
    app = apps.Config.label
    phase = 'collect'
    view = views.MapIdeaListView

    name = _('Collect phase')
    description = _('Create new ideas located on a map and comment them.')
    module_name = _('ideas collection')

    features = {
        'crud': (models.MapIdea,),
        'comment': (models.MapIdea,),
    }


class RatingPhase(phases.PhaseContent):
    app = apps.Config.label
    phase = 'rating'
    view = views.MapIdeaListView

    name = _('Rating phase')
    description = _('Get quantative feeback by rating the collected ideas.')
    module_name = _('ideas collection')

    features = {
        'rate': (models.MapIdea,)
    }


class FeedbackPhase(phases.PhaseContent):
    app = apps.Config.label
    phase = 'feedback'
    view = views.MapIdeaListView

    name = _('Feedback phase')
    description = _('Get feedback for collected ideas through rates and '
                    'comments.')
    module_name = _('ideas collection')

    features = {
        'rate': (models.MapIdea,),
        'comment': (models.MapIdea,)
    }


class CollectFeedbackPhase(phases.PhaseContent):
    app = apps.Config.label
    phase = 'collect_feedback'
    view = views.MapIdeaListView

    name = _('Collect ideas and get feedback')
    description = _('Create new ideas located on a map and get feedback '
                    'through rates and comments.')
    module_name = _('ideas collection')

    features = {
        'crud': (models.MapIdea,),
        'comment': (models.MapIdea,),
        'rate': (models.MapIdea,)
    }


phases.content.register(IssuePhase())
phases.content.register(CollectPhase())
phases.content.register(RatingPhase())
phases.content.register(FeedbackPhase())
phases.content.register(CollectFeedbackPhase())

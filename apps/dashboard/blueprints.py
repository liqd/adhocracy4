from collections import namedtuple

from django.utils.translation import ugettext_lazy as _

from apps.budgeting import phases as budgeting_phases
from apps.documents import phases as documents_phases
from apps.ideas import phases as ideas_phases

ProjectBlueprint = namedtuple(
    'ProjectBlueprint', [
        'title', 'description', 'content', 'image', 'settings_model'
    ]
)

blueprints = [
    ('brainstorming',
     ProjectBlueprint(
         title=_('Brainstorming'),
         description=_('Collect ideas, questions and input concerning '
                       'a problem or a question from a wide array of people.'),
         content=[
             ideas_phases.CollectPhase(),
         ],
         image='images/LOGO.png',
         settings_model=None,
     )),
    ('agenda-setting',
     ProjectBlueprint(
         title=_('Agenda Setting'),
         description=_('You can involve everyone in planning a meeting. '
                       'Collect ideas for an upcoming event and let your '
                       'participants vote on the topics you want to tackle.'),
         content=[
             ideas_phases.CollectPhase(),
             ideas_phases.RatingPhase(),
         ],
         image='images/LOGO.png',
         settings_model=None,
     )),
    ('text-review',
     ProjectBlueprint(
         title=_('Text Review'),
         description=_('Let participants discuss individual paragraphs of a '
                       'text. This is ideal for discussing position papers or '
                       'a mission statements with many people.'),
         content=[
             documents_phases.CreateDocumentPhase(),
             documents_phases.CommentPhase(),
         ],
         image='images/LOGO.png',
         settings_model=None,
     )),
    ('participatory-budgeting',
     ProjectBlueprint(
         title=_('Participatory budgeting'),
         description=_('TODO'),
         content=[
             budgeting_phases.RequestPhase(),
             budgeting_phases.FeedbackPhase(),
         ],
         image='images/LOGO.png',
         settings_model=None,
     )),
]


class BlueprintMixin():
    @property
    def blueprint(self):
        return dict(blueprints)[self.kwargs['blueprint_slug']]

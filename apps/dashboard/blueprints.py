from collections import namedtuple

from django.utils.translation import ugettext_lazy as _

from apps.bplan import phases as bplan_phases
from apps.budgeting import phases as budgeting_phases
from apps.documents import phases as documents_phases
from apps.extprojects import phases as extprojects_phases
from apps.ideas import phases as ideas_phases
from apps.kiezkasse import phases as kiezkasse_phases
from apps.mapideas import phases as mapideas_phases
from apps.polls import phases as poll_phases
from apps.topicprio import phases as topicprio_phases

ProjectBlueprint = namedtuple(
    'ProjectBlueprint', [
        'title', 'description', 'content', 'image', 'settings_model'
    ]
)

blueprints = [
    ('brainstorming',
     ProjectBlueprint(
         title=_('Brainstorming'),
         description=_(
             'Collect first ideas for a specific topic and comment on them.'
         ),
         content=[
             ideas_phases.CollectPhase(),
         ],
         image='images/blueprints/brainstorming.svg',
         settings_model=None,
     )),
    ('map-brainstorming',
     ProjectBlueprint(
         title=_('Spatial Brainstorming'),
         description=_(
             'Collect location specific ideas for a topic and comment on them.'
         ),
         content=[
             mapideas_phases.CollectPhase(),
         ],
         image='images/blueprints/map-brainstorming.svg',
         settings_model=('a4maps', 'AreaSettings'),
     )),
    ('map-idea-collection',
     ProjectBlueprint(
         title=_('Spatial Idea Collection'),
         description=_(
             'Collect location specific ideas that can be rated and commented.'
         ),
         content=[
             mapideas_phases.CollectPhase(),
             mapideas_phases.RatingPhase()
         ],
         image='images/blueprints/map-brainstorming.svg',
         settings_model=('a4maps', 'AreaSettings'),
     )),
    ('agenda-setting',
     ProjectBlueprint(
         title=_('Agenda Setting'),
         description=_(
             'With Agenda-Setting it’s possible to identify topics and to '
             'define mission statements. Afterwards anyone can comment and '
             'rate on different topics.'
         ),
         content=[
             ideas_phases.CollectPhase(),
             ideas_phases.RatingPhase(),
         ],
         image='images/blueprints/agenda-setting.svg',
         settings_model=None,
     )),
    ('text-review',
     ProjectBlueprint(
         title=_('Text Review'),
         description=_(
             'In the text-review it’s possible to structure draft texts '
             'co-operativly and rate and comment on them.'
         ),
         content=[
             documents_phases.CreateDocumentPhase(),
             documents_phases.CommentPhase(),
         ],
         image='images/blueprints/text-review.svg',
         settings_model=None,
     )),
    ('participatory-budgeting',
     ProjectBlueprint(
         title=_('Participatory budgeting'),
         description=_(
             'With participatory-budgeting it’s possible to make proposals '
             'with budget specifications and locate them. Afterwards anyone '
             'can comment and rate on different proposals.'
         ),
         content=[
             budgeting_phases.RequestPhase(),
             budgeting_phases.FeedbackPhase(),
         ],
         image='images/blueprints/participatory-budgeting.svg',
         settings_model=('a4maps', 'AreaSettings'),
     )),
    ('external-project',
     ProjectBlueprint(
         title=_('External project'),
         description=_(
             'External projects are handled on a different platform.'
         ),
         content=[
             extprojects_phases.ExternalPhase(),
         ],
         image='images/blueprints/external-project.svg',
         settings_model=None,
     )),
    ('poll',
     ProjectBlueprint(
         title=_('Poll'),
         description=_(
             'Create a poll with multiple questions and possible answers. '
             'Anyone can cast votes and comment on the poll.'
         ),
         content=[
             poll_phases.VotingPhase(),
         ],
         image='images/blueprints/poll.svg',
         settings_model=None,
     )),
    ('topic-prioritization',
     ProjectBlueprint(
         title=_('Topic Prioritization'),
         description=_(
             'Comment and prioritize topics.'
         ),
         content=[
             topicprio_phases.PrioritizePhase(),
         ],
         image='images/blueprints/priorization.svg',
         settings_model=None,
     )),
    ('bplan',
     ProjectBlueprint(
         title=_('Development Plan'),
         description=_('Create a statement formular for development plans'
                       ' to be embedded on external sites.'),
         content=[
             bplan_phases.StatementPhase(),
         ],
         image='images/blueprints/bplan.svg',
         settings_model=None,
     )),
    ('kiezkasse',
     ProjectBlueprint(
         title=_('Kiezkasse'),
         description=_(
             'With kiezkasse it’s possible to make proposals '
             'with budget specifications and locate them. Afterwards anyone '
             'can comment and rate on different proposals.'
         ),
         content=[
             kiezkasse_phases.RequestPhase(),
             kiezkasse_phases.FeedbackPhase(),
         ],
         image='images/blueprints/participatory-budgeting.svg',
         settings_model=('a4maps', 'AreaSettings'),
     )),
]


class BlueprintMixin:
    @property
    def blueprint(self):
        return dict(blueprints)[self.kwargs['blueprint_slug']]

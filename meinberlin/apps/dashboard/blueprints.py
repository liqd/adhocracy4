from django.utils.translation import ugettext_lazy as _

from adhocracy4.dashboard.blueprints import ProjectBlueprint
from meinberlin.apps.bplan import phases as bplan_phases
from meinberlin.apps.budgeting import phases as budgeting_phases
from meinberlin.apps.documents import phases as documents_phases
from meinberlin.apps.extprojects import phases as extprojects_phases
from meinberlin.apps.facetoface import phases as facetoface_phases
from meinberlin.apps.ideas import phases as ideas_phases
from meinberlin.apps.kiezkasse import phases as kiezkasse_phases
from meinberlin.apps.mapideas import phases as mapideas_phases
from meinberlin.apps.maptopicprio import phases as maptopicprio_phases
from meinberlin.apps.polls import phases as poll_phases
from meinberlin.apps.topicprio import phases as topicprio_phases

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
         image='images/brainstorming.svg',
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
         image='images/map-brainstorming.svg',
         settings_model=('a4maps', 'AreaSettings'),
     )),
    ('map-idea-collection',
     ProjectBlueprint(
         title=_('Spatial Idea Collection'),
         description=_(
             'Collect location specific ideas that can be rated and commented.'
         ),
         content=[
             mapideas_phases.CollectFeedbackPhase(),
         ],
         image='images/map-idea-collection.svg',
         settings_model=('a4maps', 'AreaSettings'),
     )),
    ('agenda-setting',
     ProjectBlueprint(
         title=_('Agenda Setting'),
         description=_(
             'With Agenda-Setting it’s possible to identify topics and to '
             'define mission statements. Anyone can submit topics that can be '
             'commented and rated.'
         ),
         content=[
             ideas_phases.CollectFeedbackPhase(),
         ],
         image='images/agenda-setting.svg',
         settings_model=None,
     )),
    ('text-review',
     ProjectBlueprint(
         title=_('Text Review'),
         description=_(
             'In the text-review it’s possible to structure draft texts '
             'that can be commented.'
         ),
         content=[
             documents_phases.CommentPhase(),
         ],
         image='images/text-review.svg',
         settings_model=None,
     )),
    ('participatory-budgeting',
     ProjectBlueprint(
         title=_('Participatory budgeting'),
         description=_(
             'With participatory-budgeting it’s possible to make proposals '
             'with budget specifications and locate them. Anyone can comment '
             'and rate on different proposals.'
         ),
         content=[
             budgeting_phases.RequestPhase()
         ],
         image='images/participatory-budgeting.svg',
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
         image='images/external-project.svg',
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
         image='images/poll.svg',
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
         image='images/priorization.svg',
         settings_model=None,
     )),
    ('map-topic-prioritization',
     ProjectBlueprint(
         title=_('Place Prioritization'),
         description=_(
             'Comment and prioritize places located on a map.'
         ),
         content=[
             maptopicprio_phases.PrioritizePhase(),
         ],
         image='images/place-priotization.svg',
         settings_model=('a4maps', 'AreaSettings'),
     )),
    ('bplan',
     ProjectBlueprint(
         title=_('Development Plan'),
         description=_('Create a statement formular for development plans'
                       ' to be embedded on external sites.'),
         content=[
             bplan_phases.StatementPhase(),
         ],
         image='images/bplan.svg',
         settings_model=None,
     )),
    ('kiezkasse',
     ProjectBlueprint(
         title=_('Kiezkasse'),
         description=_(
             'With kiezkasse it’s possible to make proposals '
             'with budget specifications and locate them. '
             'The proposals can be commented and rated.'
         ),
         content=[
             kiezkasse_phases.RequestFeedbackPhase(),
         ],
         image='images/kiezkasse.svg',
         settings_model=('a4maps', 'AreaSettings'),
     )),
    ('facetoface',
     ProjectBlueprint(
         title=_('Face to Face Participation'),
         description=_(
             'Share info about a face to face participation event.'
         ),
         content=[
             facetoface_phases.FaceToFacePhase(),
         ],
         image='images/kiezkasse.svg',
         settings_model=None,
     )),
]

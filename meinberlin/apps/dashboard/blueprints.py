from django.utils.translation import ugettext_lazy as _

from adhocracy4.dashboard.blueprints import ProjectBlueprint
from meinberlin.apps.budgeting import phases as budgeting_phases
from meinberlin.apps.documents import phases as documents_phases
from meinberlin.apps.ideas import phases as ideas_phases
from meinberlin.apps.kiezkasse import phases as kiezkasse_phases
from meinberlin.apps.livequestions import phases as livequestion_phases
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
    ('topic-prioritization',
     ProjectBlueprint(
         title=_('Topic Priorization'),
         description=_(
             'Comment and prioritize topics.'
         ),
         content=[
             topicprio_phases.PrioritizePhase(),
         ],
         image='images/priorization.svg',
         settings_model=None,
     )),
    ('participatory-budgeting',
     ProjectBlueprint(
         title=_('Participatory budgeting (1 phase)'),
         description=_(
             'Proposals can be located on a map and a budget can be added. '
             'Proposals can be commented and rated.'
         ),
         content=[
             budgeting_phases.RequestPhase()
         ],
         image='images/participatory-budgeting-1.svg',
         settings_model=('a4maps', 'AreaSettings'),
     )),
    ('participatory-budgeting-2-phases',
     ProjectBlueprint(
         title=_('Participatory budgeting (2 phase)'),
         description=_(
             'Proposals can be located on a map and a budget can be added. '
             'Proposals can be commented and rated in 2 phases.'
         ),
         content=[
             budgeting_phases.CollectPhase(),
             budgeting_phases.RatingPhase(),
         ],
         image='images/participatory-budgeting-2.svg',
         settings_model=('a4maps', 'AreaSettings'),
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
    ('interactive-event',
     ProjectBlueprint(
         title=_('Interactive Event'),
         description=_(
             'The participants of an event can ask their questions online. '
             'Other participants can support the question. You as the '
             'moderator can sort the questions by support or '
             'characteristic.'
         ),
         content=[
             livequestion_phases.IssuePhase(),
         ],
         image='images/interactive-event.svg',
         settings_model=None,
     )),
]

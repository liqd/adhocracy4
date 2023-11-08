from django.utils.translation import gettext_lazy as _

from adhocracy4.dashboard.blueprints import ProjectBlueprint
from adhocracy4.polls import phases as poll_phases
from meinberlin.apps.budgeting import phases as budgeting_phases
from meinberlin.apps.documents import phases as documents_phases
from meinberlin.apps.ideas import phases as ideas_phases
from meinberlin.apps.livequestions import phases as livequestion_phases
from meinberlin.apps.mapideas import phases as mapideas_phases
from meinberlin.apps.maptopicprio import phases as maptopicprio_phases
from meinberlin.apps.topicprio import phases as topicprio_phases

blueprints = [
    (
        "brainstorming",
        ProjectBlueprint(
            title=_("Brainstorming"),
            description=_(
                "Participants can submit their own ideas and discuss the ideas "
                "of others."
            ),
            content=[
                ideas_phases.CollectPhase(),
            ],
            image="images/brainstorming.svg",
            settings_model=None,
            type="BS",
        ),
    ),
    (
        "map-brainstorming",
        ProjectBlueprint(
            title=_("Spatial Brainstorming"),
            description=_(
                "Participants can submit their own ideas and locate them on a "
                "map. They can also discuss the ideas of others."
            ),
            content=[
                mapideas_phases.CollectPhase(),
            ],
            image="images/map-brainstorming.svg",
            settings_model=("a4maps", "AreaSettings"),
            type="MBS",
        ),
    ),
    (
        "idea-collection",
        ProjectBlueprint(
            title=_("Idea Collection"),
            description=_(
                "Participants can submit their own ideas and discuss and rate "
                "(pro/contra) the ideas of others."
            ),
            content=[
                ideas_phases.CollectFeedbackPhase(),
            ],
            image="images/agenda-setting.svg",
            settings_model=None,
            type="IC",
        ),
    ),
    (
        "map-idea-collection",
        ProjectBlueprint(
            title=_("Spatial Idea Collection"),
            description=_(
                "Participants can submit their own ideas and locate them on a "
                "map. They can also discuss and rate (pro/contra) the ideas of "
                "others."
            ),
            content=[
                mapideas_phases.CollectFeedbackPhase(),
            ],
            image="images/map-idea-collection.svg",
            settings_model=("a4maps", "AreaSettings"),
            type="MIC",
        ),
    ),
    (
        "participatory-budgeting",
        ProjectBlueprint(
            title=_("Participatory budgeting (1 phase)"),
            description=_(
                "Participants can submit their own proposals, mark them on a "
                "map, and add a budget. The proposals of others can be discussed "
                "and supported."
            ),
            content=[budgeting_phases.RequestSupportPhase()],
            image="images/participatory-budgeting-1.svg",
            settings_model=("a4maps", "AreaSettings"),
            type="PB",
        ),
    ),
    (
        "participatory-budgeting-2-phases",
        ProjectBlueprint(
            title=_("Participatory budgeting (2 phase)"),
            description=_(
                "In a first phase, participants can submit their own proposals, "
                "mark them on a map, and add a budget. The proposals of others "
                "can be discussed and in a second phase supported."
            ),
            content=[
                budgeting_phases.CollectPhase(),
                budgeting_phases.BudgetingTwoSupportPhase(),
            ],
            image="images/participatory-budgeting-2.svg",
            settings_model=("a4maps", "AreaSettings"),
            type="PB2",
        ),
    ),
    (
        "participatory-budgeting-3-phases",
        ProjectBlueprint(
            title=_("Participatory budgeting (3 phase)"),
            description=_(
                "In a first phase, participants can submit their own "
                "suggestions, mark them on a map, and add a budget. The "
                "proposals of others can be discussed. In a second phase "
                "proposals can be supported. In the third phase, participants "
                "vote on the shortlisted proposals.  "
            ),
            content=[
                budgeting_phases.CollectPhase(),
                budgeting_phases.SupportPhase(),
                budgeting_phases.VotingPhase(),
            ],
            # The icon has to be updated:
            image="images/participatory-budgeting-3.svg",
            settings_model=("a4maps", "AreaSettings"),
            type="PB3",
        ),
    ),
    (
        "prioritization",
        ProjectBlueprint(
            title=_("Prioritization"),
            description=_(
                "Participants can discuss and rate (pro/contra) previously added "
                "ideas and topics. Participants cannot add ideas or topics."
            ),
            content=[
                topicprio_phases.PrioritizePhase(),
            ],
            image="images/priorization.svg",
            settings_model=None,
            type="TP",
        ),
    ),
    (
        "map-topic-prioritization",
        ProjectBlueprint(
            title=_("Spatial Prioritization"),
            description=_(
                "Participants can discuss and rate (pro/contra) ideas and topics "
                "previously added to a map. Participants cannot add ideas or "
                "topics."
            ),
            content=[
                maptopicprio_phases.PrioritizePhase(),
            ],
            image="images/place-priotization.svg",
            settings_model=("a4maps", "AreaSettings"),
            type="MTP",
        ),
    ),
    (
        "text-review",
        ProjectBlueprint(
            title=_("Text Review"),
            description=_(
                "Participants can discuss the paragraphs of a text that you "
                "added beforehand."
            ),
            content=[
                documents_phases.CommentPhase(),
            ],
            image="images/text-review.svg",
            settings_model=None,
            type="TR",
        ),
    ),
    (
        "poll",
        ProjectBlueprint(
            title=_("Poll"),
            description=_(
                "Participants can answer open and multiple choice questions "
                "and can comment on the poll"
            ),
            content=[
                poll_phases.VotingPhase(),
            ],
            image="images/poll.svg",
            settings_model=None,
            type="PO",
        ),
    ),
    (
        "interactive-event",
        ProjectBlueprint(
            title=_("Interactive Event"),
            description=_(
                "The participants of an event can ask their questions online. "
                "Other participants can support the question. The moderator can "
                "sort the questions by support or affiliation."
            ),
            content=[
                livequestion_phases.IssuePhase(),
            ],
            image="images/interactive-event.svg",
            settings_model=None,
            type="IE",
        ),
    ),
]

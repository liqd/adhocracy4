import rules
from rules.predicates import is_superuser

from adhocracy4.modules import predicates as module_predicates
from adhocracy4.organisations.predicates import is_initiator
from adhocracy4.projects.predicates import is_prj_group_member

rules.add_perm(
    "meinberlin_offlineevents.list_offlineevent",
    is_superuser | is_initiator | is_prj_group_member,
)

rules.add_perm(
    "meinberlin_offlineevents.view_offlineevent", module_predicates.is_allowed_view_item
)

rules.add_perm(
    "meinberlin_offlineevents.add_offlineevent",
    is_superuser | is_initiator | is_prj_group_member,
)

rules.add_perm(
    "meinberlin_offlineevents.change_offlineevent",
    is_superuser | is_initiator | is_prj_group_member,
)

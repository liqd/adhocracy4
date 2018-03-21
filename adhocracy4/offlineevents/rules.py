import rules

from adhocracy4.modules import predicates as module_predicates

rules.add_perm(
    'a4offlineevents.view_offlineevent',
    module_predicates.is_allowed_view_item
)

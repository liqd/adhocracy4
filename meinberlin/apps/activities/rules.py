import rules

from adhocracy4.modules import predicates as module_predicates

rules.add_perm(
    'meinberlin_activities.change_activity',
    module_predicates.is_allowed_moderate_project
)

rules.add_perm(
    'meinberlin_activities.view_activity',
    module_predicates.is_allowed_view_item
)

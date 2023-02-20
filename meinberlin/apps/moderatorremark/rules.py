import rules

from adhocracy4.modules import predicates as module_predicates

rules.add_perm(
    "meinberlin_moderatorremark.add_moderatorremark",
    module_predicates.is_allowed_moderate_project,
)

rules.add_perm(
    "meinberlin_moderatorremark.change_moderatorremark",
    module_predicates.is_allowed_moderate_project,
)

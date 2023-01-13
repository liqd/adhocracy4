import rules

from adhocracy4.modules import predicates as module_predicates

rules.add_perm(
    "meinberlin_maptopicprio.add_maptopic", module_predicates.is_allowed_crud_project
)

rules.add_perm(
    "meinberlin_maptopicprio.change_maptopic", module_predicates.is_allowed_crud_project
)

rules.add_perm(
    "meinberlin_maptopicprio.view_maptopic",
    (
        module_predicates.is_allowed_moderate_project
        | module_predicates.is_allowed_view_item
    ),
)

rules.add_perm(
    "meinberlin_maptopicprio.rate_maptopic", module_predicates.is_allowed_rate_item
)

rules.add_perm(
    "meinberlin_maptopicprio.comment_maptopic",
    module_predicates.is_allowed_comment_item,
)

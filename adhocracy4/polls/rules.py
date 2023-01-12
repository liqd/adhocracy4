import rules

from adhocracy4.modules import predicates as module_predicates

from .predicates import is_allowed_add_vote

rules.add_perm("a4polls.change_poll", module_predicates.is_allowed_crud_project)

rules.add_perm(
    "a4polls.view_poll",
    (
        module_predicates.is_allowed_moderate_project
        | module_predicates.is_allowed_view_item
    ),
)

rules.add_perm("a4polls.comment_poll", module_predicates.is_allowed_comment_item)

rules.add_perm("a4polls.add_vote", is_allowed_add_vote)

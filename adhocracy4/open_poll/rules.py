import rules

from adhocracy4.modules import predicates as module_predicates

from .predicates import is_allowed_add_vote

"""The change, view and comment permissions are derived from the model name, thus
they have to be called openpoll instead of open_poll"""
rules.add_perm("a4open_poll.change_openpoll", module_predicates.is_allowed_crud_project)

rules.add_perm(
    "a4open_poll.view_openpoll",
    (
        module_predicates.is_allowed_moderate_project
        | module_predicates.is_allowed_view_item
    ),
)

rules.add_perm(
    "a4open_poll.comment_openpoll", module_predicates.is_allowed_comment_item
)

rules.add_perm("a4open_poll.add_vote", is_allowed_add_vote)

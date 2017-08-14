import rules
from rules.predicates import is_superuser

from adhocracy4.modules import predicates as module_predicates
from meinberlin.apps.contrib import predicates as contrib_predicates

from . import models

rules.add_perm(
    'meinberlin_polls.change_poll',
    is_superuser | module_predicates.is_context_initiator
)

rules.add_perm(
    'meinberlin_polls.view_poll',
    (module_predicates.is_project_admin |
     (module_predicates.is_allowed_view_item &
      contrib_predicates.has_context_started))
)

rules.add_perm(
    'meinberlin_polls.comment_poll',
    module_predicates.is_allowed_comment_item
)


# Note: Those rules are checked from api.py which uses Put-As-Create.
# Thus the is_allowed_add_item has to be checked in the add and change case.
# It has to be ensured that the permission is always checked against a module
# never a Vote object.
rules.add_perm(
    'meinberlin_polls.add_vote',
    module_predicates.is_allowed_add_item(models.Vote)
)

rules.add_perm(
    'meinberlin_polls.change_vote',
    module_predicates.is_allowed_add_item(models.Vote)
)

import rules

from rules.predicates import is_superuser

from adhocracy4.modules import predicates as module_predicates

from . import models


rules.add_perm(
    'meinberlin_polls.change_poll',
    is_superuser | module_predicates.is_context_initiator
)

rules.add_perm(
    'meinberlin_polls.view_poll',
    module_predicates.is_public_context
)

rules.add_perm(
    'meinberlin_polls.comment_poll',
    module_predicates.is_allowed_comment_item
)

rules.add_perm(
    'meinberlin_polls.add_vote',
    module_predicates.is_allowed_add_item(models.Vote)
)

rules.add_perm(
    'meinberlin_polls.change_vote',
    module_predicates.is_allowed_add_item(models.Vote)
)

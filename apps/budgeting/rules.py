import rules

from adhocracy4.modules import predicates as module_predicates

from . import models


rules.add_perm(
    'meinberlin_budgeting.view_proposal',
    module_predicates.is_allowed_view_item
)


rules.add_perm(
    'meinberlin_budgeting.propose_proposal',
    module_predicates.is_allowed_create_item(models.Proposal)
)

rules.add_perm(
    'meinberlin_budgeting.rate_proposal',
    module_predicates.is_allowed_rate_item
)


rules.add_perm(
    'meinberlin_budgeting.comment_proposal',
    module_predicates.is_allowed_comment_item
)


rules.add_perm(
    'meinberlin_budgeting.modify_proposal',
    module_predicates.is_allowed_modify_item
)


rules.add_perm(
    'meinberlin_budgeting.moderate_proposal',
    module_predicates.is_context_moderator
)

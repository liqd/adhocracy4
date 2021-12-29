import rules

from adhocracy4.modules import predicates as module_predicates
from adhocracy4.phases import predicates as phase_predicates

from . import models
from .predicates import is_allowed_delete_vote
from .predicates import is_allowed_vote_proposal

rules.add_perm(
    'meinberlin_budgeting.view_proposal',
    module_predicates.is_allowed_view_item
)


rules.add_perm(
    'meinberlin_budgeting.add_proposal',
    module_predicates.is_allowed_add_item(models.Proposal)
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
    'meinberlin_budgeting.change_proposal',
    module_predicates.is_allowed_change_item
)


rules.add_perm(
    'meinberlin_budgeting.moderate_proposal',
    module_predicates.is_context_moderator |
    module_predicates.is_context_initiator
)

rules.add_perm(
    'meinberlin_budgeting.vote_proposal',
    is_allowed_vote_proposal
)

rules.add_perm(
    'meinberlin_budgeting.add_vote',
    phase_predicates.phase_allows_add_vote(models.Proposal)
)

rules.add_perm(
    'meinberlin_budgeting.delete_vote',
    is_allowed_delete_vote
)

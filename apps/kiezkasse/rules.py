import rules

from adhocracy4.modules import predicates as module_predicates

from . import models


rules.add_perm(
    'meinberlin_kiezkasse.view_proposal',
    module_predicates.is_allowed_view_item
)


rules.add_perm(
    'meinberlin_kiezkasse.add_proposal',
    module_predicates.is_allowed_add_item(models.Proposal)
)

rules.add_perm(
    'meinberlin_kiezkasse.rate_proposal',
    module_predicates.is_allowed_rate_item
)


rules.add_perm(
    'meinberlin_kiezkasse.comment_proposal',
    module_predicates.is_allowed_comment_item
)


rules.add_perm(
    'meinberlin_kiezkasse.change_proposal',
    module_predicates.is_allowed_change_item
)

rules.add_perm(
    'meinberlin_kiezkasse.moderate_proposal',
    module_predicates.is_context_moderator
)

import rules

from adhocracy4.modules import predicates as module_predicates

from . import models


rules.add_perm(
    'meinberlin_mapideas.view_idea',
    module_predicates.is_allowed_view_item
)

rules.add_perm(
    'meinberlin_mapideas.propose_idea',
    module_predicates.is_allowed_create_item(models.MapIdea)
)

rules.add_perm(
    'meinberlin_mapideas.rate_idea',
    module_predicates.is_allowed_rate_item
)

rules.add_perm(
    'meinberlin_mapideas.comment_idea',
    module_predicates.is_allowed_comment_item
)


rules.add_perm(
    'meinberlin_mapideas.modify_idea',
    module_predicates.is_allowed_modify_item
)

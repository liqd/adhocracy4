import rules
from rules.predicates import is_superuser

from adhocracy4.modules import predicates as module_predicates

rules.add_perm(
    "meinberlin_moderatorremark.add_moderatorremark",
    is_superuser
    | module_predicates.is_context_moderator
    | module_predicates.is_context_initiator,
)

rules.add_perm(
    "meinberlin_moderatorremark.change_moderatorremark",
    is_superuser
    | module_predicates.is_context_moderator
    | module_predicates.is_context_initiator,
)

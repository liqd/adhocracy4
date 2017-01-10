import rules
from rules.predicates import is_superuser

from adhocracy4.modules.predicates import is_context_initiator
from adhocracy4.modules.predicates import is_context_member
from adhocracy4.modules.predicates import is_context_moderator
from adhocracy4.modules.predicates import is_public_context
from adhocracy4.phases.predicates import phase_allows_rate

rules.add_perm('meinberlin_ideas.rate_idea',
               is_superuser | is_context_moderator | is_context_initiator |
               (is_context_member & phase_allows_rate))

rules.add_perm('meinberlin_ideas.view_idea',
               is_superuser | is_context_moderator | is_context_initiator |
               is_context_member | is_public_context)

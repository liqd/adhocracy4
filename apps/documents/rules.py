import rules
from rules.predicates import is_superuser

from adhocracy4.modules.predicates import is_context_initiator
from adhocracy4.modules.predicates import is_context_member
from adhocracy4.modules.predicates import is_context_moderator
from adhocracy4.modules.predicates import is_public_context


rules.add_perm('meinberlin_documents.view',
               is_superuser | is_context_moderator | is_context_initiator |
               is_context_member | is_public_context)


rules.add_perm('meinberlin_documents.create',
               is_superuser | is_context_moderator | is_context_initiator)

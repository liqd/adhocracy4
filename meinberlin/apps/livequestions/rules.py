import rules
from rules.predicates import is_superuser

from adhocracy4.modules.predicates import is_context_initiator
from adhocracy4.modules.predicates import is_context_moderator
from adhocracy4.phases.predicates import phase_allows_add

from .models import LiveQuestion

rules.add_perm('meinberlin_livequestions.change_livequestion',
               is_superuser | is_context_moderator | is_context_initiator)

rules.add_perm('meinberlin_livequestions.add_livequestion',
               phase_allows_add(LiveQuestion))

rules.add_perm('meinberlin_livequestions.view_livequestion',
               rules.always_allow)


rules.add_perm('meinberlin_livequestions.moderate_livequestions',
               is_superuser | is_context_moderator | is_context_initiator)

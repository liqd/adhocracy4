import rules
from rules.predicates import is_superuser

from adhocracy4.organisations.predicates import is_initiator

from .predicates import is_live, is_member, is_public


rules.add_perm('a4projects.add_project',
               is_superuser | is_initiator)


rules.add_perm('a4projects.change_project',
               is_superuser | is_initiator)


rules.add_perm('a4projects.view_project',
               is_superuser | is_initiator |
               ((is_public | is_member) & is_live))

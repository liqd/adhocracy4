import rules
from rules.predicates import is_superuser

from adhocracy4.projects.predicates import is_moderator
from adhocracy4.organisations.predicates import is_initiator


rules.remove_perm('a4projects.change_project')
rules.add_perm('a4projects.change_project',
               is_superuser | is_initiator | is_moderator)

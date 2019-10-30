import rules
from rules.predicates import is_superuser

from adhocracy4.organisations.predicates import is_initiator
from adhocracy4.organisations.predicates import is_org_group_member

from .predicates import is_live
from .predicates import is_member
from .predicates import is_prj_group_member
from .predicates import is_public

rules.add_perm('a4projects.add_project',
               is_superuser | is_initiator | is_org_group_member)


rules.add_perm('a4projects.change_project',
               is_superuser | is_initiator | is_prj_group_member)


rules.add_perm('a4projects.view_project',
               is_superuser | is_initiator | is_prj_group_member |
               ((is_public | is_member) & is_live))

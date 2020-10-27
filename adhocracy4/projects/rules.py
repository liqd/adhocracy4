import rules
from rules.predicates import is_superuser

from adhocracy4.organisations.predicates import is_initiator
from adhocracy4.organisations.predicates import is_org_group_member
from adhocracy4.organisations.predicates import is_org_member

from .predicates import is_live
from .predicates import is_moderator
from .predicates import is_prj_group_member
from .predicates import is_project_member
from .predicates import is_public
from .predicates import is_semipublic

rules.add_perm('a4projects.add_project',
               is_superuser | is_initiator | is_org_group_member)


rules.add_perm('a4projects.change_project',
               is_superuser | is_initiator | is_prj_group_member)


rules.add_perm('a4projects.view_project',
               is_superuser | is_initiator | is_prj_group_member |
               is_moderator | ((is_public | is_semipublic | is_org_member |
                                is_project_member) & is_live))


rules.add_perm('a4projects.participate_in_project',
               is_superuser | is_initiator | is_prj_group_member |
               is_moderator | ((is_public | is_org_member |
                                is_project_member) & is_live))

rules.add_perm('a4projects.delete_project',
               is_superuser | is_initiator)

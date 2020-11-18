import rules
from rules.predicates import is_superuser

from adhocracy4.organisations.predicates import is_initiator
from adhocracy4.projects.predicates import is_live
from adhocracy4.projects.predicates import is_moderator
from adhocracy4.projects.predicates import is_prj_group_member
from adhocracy4.projects.predicates import is_project_member
from adhocracy4.projects.predicates import is_public
from adhocracy4.projects.predicates import is_semipublic

rules.remove_perm('a4projects.change_project')
rules.add_perm('a4projects.change_project',
               is_superuser | is_initiator |
               is_moderator | is_prj_group_member)

rules.remove_perm('a4projects.view_project')
rules.add_perm('a4projects.view_project',
               is_superuser | is_initiator |
               is_moderator | is_prj_group_member |
               ((is_public | is_semipublic | is_project_member)
                & is_live))

rules.set_perm('a4projects.participate_in_project',
               is_superuser | is_initiator | is_moderator |
               ((is_public | is_project_member) & is_live))

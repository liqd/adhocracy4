import rules

from adhocracy4.modules import predicates as module_predicates

rules.set_perm(
    'a4polls.change_poll',
    module_predicates.is_project_admin
)

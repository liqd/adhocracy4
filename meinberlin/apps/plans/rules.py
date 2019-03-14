import rules
from rules.predicates import is_superuser

from adhocracy4.organisations.predicates import is_initiator
from adhocracy4.organisations.predicates import is_org_group_member

rules.add_perm(
    'meinberlin_plans.list_plan',
    rules.always_allow
)

rules.add_perm(
    'meinberlin_plans.view_plan',
    rules.always_allow
)

rules.add_perm(
    'meinberlin_plans.add_plan',
    is_superuser | is_initiator | is_org_group_member
)

rules.add_perm(
    'meinberlin_plans.change_plan',
    is_superuser | is_initiator | is_org_group_member
)

rules.add_perm(
    'meinberlin_plans.export_plan',
    is_superuser | is_initiator
)

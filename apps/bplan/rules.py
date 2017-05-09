import rules

from adhocracy4.organisations.predicates import is_initiator

rules.add_perm(
    'meinberlin_bplan.add_bplan',
    is_initiator
)


rules.add_perm(
    'meinberlin_bplan.change_bplan',
    is_initiator
)

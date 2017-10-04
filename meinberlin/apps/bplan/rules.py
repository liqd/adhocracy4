import rules

from adhocracy4.modules import predicates as module_predicates
from adhocracy4.organisations.predicates import is_initiator
from adhocracy4.phases import predicates as phase_predicates

from . import models

rules.add_perm(
    'meinberlin_bplan.add_bplan',
    is_initiator
)

rules.add_perm(
    'meinberlin_bplan.change_bplan',
    is_initiator
)

rules.add_perm(
    'meinberlin_bplan.add_statement',
    module_predicates.is_live_context &
    phase_predicates.phase_allows_add(models.Statement)
)

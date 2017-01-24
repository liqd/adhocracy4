import rules
from rules.predicates import is_superuser

from .predicates import is_initiator

rules.add_perm('meinberlin_organisations.modify_organisation',
               is_superuser | is_initiator)

rules.add_perm('meinberlin_organisations.initiate_project',
               is_superuser | is_initiator)

import rules
from rules.predicates import is_superuser

rules.add_perm('meinberlin_organisations.change_organisation',
               is_superuser)

import rules
from rules.predicates import is_superuser

rules.add_perm("meinberlin_projectcontainers.add_container", is_superuser)

import rules

rules.add_perm(
    'meinberlin_initiators.request',
    rules.is_authenticated
)

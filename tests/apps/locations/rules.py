import rules

from adhocracy4.modules.predicates import is_allowed_view_item

rules.add_perm('a4test_locations.view_location', is_allowed_view_item)

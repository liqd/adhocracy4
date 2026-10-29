import rules

from adhocracy4.modules.predicates import is_allowed_moderate_project

rules.add_perm("a4moderation.moderate_project", is_allowed_moderate_project)

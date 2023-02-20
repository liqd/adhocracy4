import rules

from adhocracy4.modules.predicates import is_allowed_moderate_project
from adhocracy4.phases.predicates import phase_allows_add

from .models import LiveQuestion

rules.add_perm(
    "meinberlin_livequestions.change_livequestion",
    is_allowed_moderate_project,
)

rules.add_perm(
    "meinberlin_livequestions.add_livequestion", phase_allows_add(LiveQuestion)
)

rules.add_perm("meinberlin_livequestions.view_livequestion", rules.always_allow)


rules.add_perm(
    "meinberlin_livequestions.moderate_livequestions",
    is_allowed_moderate_project,
)

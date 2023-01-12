import rules

from adhocracy4.modules import predicates as module_predicates
from adhocracy4.phases import predicates as phase_predicates

from . import models


@rules.predicate
def is_allowed_add_vote(user, poll):
    if poll:
        module = poll.module
        return module_predicates.is_allowed_moderate_project(user, module) | (
            module_predicates.is_context_member(user, module)
            & module_predicates.is_live_context(user, module)
            & phase_predicates.phase_allows_add(models.Vote)(user, module)
        )
    return False

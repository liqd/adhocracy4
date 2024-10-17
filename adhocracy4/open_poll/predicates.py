import rules

from adhocracy4.modules import predicates as module_predicates
from adhocracy4.phases import predicates as phase_predicates

from . import models
from .models import OpenPoll


@rules.predicate
def allows_unregistered_users(poll: OpenPoll) -> bool:
    """Test if poll allows unregistered users to participate.
    In private and semi-private projects allow_unregistered_users has no effect as they require
    a user account to interact with by design."""
    return poll.module.project.is_public and poll.allow_unregistered_users


@rules.predicate
def is_allowed_add_vote(user, poll: OpenPoll) -> bool:
    if poll:
        module = poll.module
        return module_predicates.is_allowed_moderate_project(user, module) | (
            (
                module_predicates.is_context_member(user, module)
                | allows_unregistered_users(poll)
            )
            & module_predicates.is_live_context(user, module)
            & phase_predicates.phase_allows_add(models.Vote)(user, module)
        )
    return False

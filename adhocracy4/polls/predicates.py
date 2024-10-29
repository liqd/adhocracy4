import rules

from adhocracy4.modules import predicates as module_predicates
from adhocracy4.modules.models import Module
from adhocracy4.phases import predicates as phase_predicates
from adhocracy4.polls.models import Poll
from adhocracy4.polls.models import Vote


@rules.predicate
def allows_unregistered_users(poll: Poll) -> bool:
    """Tests if poll allows unregistered users to participate.
    In private and semi-private projects allow_unregistered_users has no effect as they require
    a user account to interact with by design."""
    return poll.module.project.is_public and poll.allow_unregistered_users


@rules.predicate
def is_allowed_add_vote(user, poll: Poll | Module) -> bool:
    """Tests if a user is allowed to vote on the poll. Due to the structure of the
    PollViewSet this function could also receive a Module if someone attempts to post
    a new Poll instead of a Vote. Polls are created automatically through the dashboard
    and also are not supposed to be created by regular users, therefore we don't allow
    the Module class here."""
    if isinstance(poll, Poll):
        module = poll.module
        return module_predicates.is_allowed_moderate_project(user, module) | (
            (
                module_predicates.is_context_member(user, module)
                | allows_unregistered_users(poll)
            )
            & module_predicates.is_live_context(user, module)
            & phase_predicates.phase_allows_add(Vote)(user, module)
        )
    return False

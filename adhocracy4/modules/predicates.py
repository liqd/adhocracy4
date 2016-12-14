import rules

from adhocracy4.organisations.predicates import is_initiator
from adhocracy4.projects.predicates import is_member, is_moderator, is_public


@rules.predicate
def is_context_initiator(user, item):
    return is_initiator(user, item.project)


@rules.predicate
def is_context_moderator(user, item):
    return is_moderator(user, item.project)


@rules.predicate
def is_context_member(user, item):
    return is_member(user, item.project)


@rules.predicate
def is_owner(user, item):
    return item.creator == user


@rules.predicate
def is_public_context(user, item):
    return is_public(user, item.project)

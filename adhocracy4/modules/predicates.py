import rules

from rules import predicates as rules_predicates

from adhocracy4.organisations.predicates import is_initiator
from adhocracy4.phases import predicates as phase_predicates
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


@rules.predicate
def is_project_admin(user, item):
    return (rules_predicates.is_superuser(user) |
            is_context_moderator(user, item) |
            is_context_initiator(user, item))


@rules.predicate
def is_allowed_view_item(user, item):
    return (is_project_admin(user, item) |
            is_context_member(user, item) |
            is_public_context(user, item))


def is_allowed_create_item(item_class):
    @rules.predicate
    def _create_item(user, item):
        return (is_project_admin(user, item) |
                (is_context_member(user, item) &
                 phase_predicates.phase_allows_create(item_class)))
    return _create_item


@rules.predicate
def is_allowed_rate_item(user, item):
    return (is_project_admin(user, item) |
            (is_context_member(user, item) &
             phase_predicates.phase_allows_rate(user, item)))


@rules.predicate
def is_allowed_comment_item(user, item):
    return (is_project_admin(user, item) |
            (is_context_member(user, item) &
             phase_predicates.phase_allows_comment(user, item)))


@rules.predicate
def is_allowed_modify_item(user, item):
    return (is_project_admin(user, item) |
            (is_context_member(user, item) &
             is_owner(user, item) &
             phase_predicates.phase_allows_modify(user, item)))

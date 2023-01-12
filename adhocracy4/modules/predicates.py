import warnings

import rules
from rules import predicates as rules_predicates

from adhocracy4.organisations.predicates import is_initiator
from adhocracy4.organisations.predicates import is_org_member
from adhocracy4.phases import predicates as phase_predicates
from adhocracy4.projects.predicates import is_live
from adhocracy4.projects.predicates import is_moderator
from adhocracy4.projects.predicates import is_prj_group_member
from adhocracy4.projects.predicates import is_project_member
from adhocracy4.projects.predicates import is_public
from adhocracy4.projects.predicates import is_semipublic


# Predicates testing roles
@rules.predicate
def is_context_initiator(user, item):
    if item:
        if hasattr(item, "project"):
            return is_initiator(user, item.project)
        else:
            return is_initiator(user, item)
    return False


@rules.predicate
def is_context_moderator(user, item):
    if item:
        if hasattr(item, "project"):
            return is_moderator(user, item.project)
        else:
            return is_moderator(user, item)
    return False


@rules.predicate
def is_context_group_member(user, item):
    if item:
        if hasattr(item, "project"):
            return is_prj_group_member(user, item.project)
        else:
            return is_prj_group_member(user, item)


@rules.predicate
def is_context_member(user, item):
    """Return if normal user is project participant or org member.


    In public projects every registered user is a participant.
    In private or semi-public projects only invited participants are
    participants.
    """
    if item:
        return is_project_member(user, item.project) | is_org_member(
            user, item.project.organisation
        )
    return False


@rules.predicate
def is_owner(user, item):
    if item:
        return item.creator == user
    return False


# Predicates testing context
@rules.predicate
def is_public_context(user, item):
    if item:
        return is_public(user, item.project) | is_semipublic(user, item.project)
    return False


@rules.predicate
def is_live_context(user, item):
    if item:
        return is_live(user, item.project)
    return False


# Predicates testing if user is allowed to do sth. in project
@rules.predicate
def is_allowed_moderate_project(user, item):
    """Return if user is allowed to moderate project of item."""
    if item:
        return (
            rules_predicates.is_superuser(user)
            | is_context_moderator(user, item)
            | is_context_initiator(user, item)
            | is_context_group_member(user, item)
        )
    return False


@rules.predicate
def is_allowed_crud_project(user, item):
    """Return if user is allowed to change project of item."""
    if item:
        return (
            rules_predicates.is_superuser(user)
            | is_context_initiator(user, item)
            | is_context_group_member(user, item)
        )
    return False


@rules.predicate
def is_project_admin(user, item):
    """Return if user is allowed to moderate project.

    Attention: This method is _deprecated_ as it was named confusingly.
    Now either use is_allowed_moderate_project or is_allowed_crud_project
    """
    warnings.warn(
        "is_project_admin is deprecated; use is_allowed_moderate_project.",
        DeprecationWarning,
    )
    return is_allowed_moderate_project(user, item)


# Predicates testing if user is allowed to do that on the item
# in the current phase; bringing together all info
@rules.predicate
def is_allowed_view_item(user, item):
    if item:
        return is_allowed_moderate_project(user, item) | (
            (is_context_member(user, item) | is_public_context(user, item))
            & is_live_context(user, item)
        )
    return False


def is_allowed_add_item(item_class):
    @rules.predicate
    def _add_item(user, module):
        if module:
            return is_allowed_moderate_project(user, module) | (
                is_context_member(user, module)
                & is_live_context(user, module)
                & phase_predicates.phase_allows_add(item_class)(user, module)
            )
        return False

    return _add_item


@rules.predicate
def is_allowed_rate_item(user, item):
    if item:
        return is_allowed_moderate_project(user, item) | (
            is_context_member(user, item)
            & is_live_context(user, item)
            & phase_predicates.phase_allows_rate(user, item)
        )
    return False


@rules.predicate
def is_allowed_comment_item(user, item):
    if item:
        return is_allowed_moderate_project(user, item) | (
            is_context_member(user, item)
            & is_live_context(user, item)
            & phase_predicates.phase_allows_comment(user, item)
        )
    return False


@rules.predicate
def is_allowed_change_item(user, item):
    if item:
        return is_allowed_moderate_project(user, item) | (
            is_context_member(user, item)
            & is_live_context(user, item)
            & is_owner(user, item)
            & phase_predicates.phase_allows_change(user, item)
        )
    return False


def module_is_between_phases(past_phase_type, future_phase_type, module):
    return (
        module.phases.active_phases().count() == 0
        and past_phase_type in [phase.type for phase in module.phases.past_phases()]
        and future_phase_type in [phase.type for phase in module.phases.future_phases()]
    )

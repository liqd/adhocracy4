import rules
from rules import predicates as rules_predicates

from adhocracy4.modules.predicates import is_allowed_moderate_project
from adhocracy4.modules.predicates import is_context_group_member
from adhocracy4.modules.predicates import is_context_initiator
from adhocracy4.modules.predicates import is_context_member
from adhocracy4.modules.predicates import is_context_moderator
from adhocracy4.modules.predicates import is_live_context
from adhocracy4.modules.predicates import is_public_context
from adhocracy4.modules.predicates import module_is_between_phases
from adhocracy4.phases.predicates import has_feature_active
from adhocracy4.phases.predicates import phase_allows_delete_vote
from adhocracy4.phases.predicates import phase_allows_vote


@rules.predicate
def is_allowed_vote_proposal(user, proposal):
    return rules_predicates.is_superuser(user) | (
        (not proposal.is_archived)
        & phase_allows_vote(user, proposal)
        & is_live_context(user, proposal)
    )


@rules.predicate
def is_allowed_delete_vote(user, vote):
    return rules_predicates.is_superuser(user) | (
        (not vote.content_object.is_archived)
        & phase_allows_delete_vote(user, vote)
        & is_live_context(user, vote.content_object)
    )


@rules.predicate
def phase_allows_support(user, item):
    if item:
        return has_feature_active(item.module, item.__class__, "support")
    return False


@rules.predicate
def is_allowed_support_item(user, item):
    if item:
        return is_allowed_moderate_project(user, item) | (
            (not item.is_archived)
            & is_context_member(user, item)
            & is_live_context(user, item)
            & phase_allows_support(user, item)
        )
    return False


@rules.predicate
def phase_allows_view_support(module, item_class):
    if module:
        return has_feature_active(
            module, item_class, "support"
        ) | module_is_between_phases(
            "meinberlin_budgeting:support", "meinberlin_budgeting:voting", module
        )
    return False


@rules.predicate
def is_allowed_view_support(item_class):
    """Admins, moderators, initiators and group members can see support at any time."""

    @rules.predicate
    def _view_support(user, module):
        if module:
            return module.has_feature("support", item_class) & (
                is_allowed_moderate_project(user, module)
                | (
                    (is_public_context(user, module) | is_context_member(user, module))
                    & is_live_context(user, module)
                    & (
                        phase_allows_view_support(module, item_class)
                        | (
                            module.module_has_finished
                            and not module.has_feature("vote", item_class)
                        )
                    )
                )
            )
        return False

    return _view_support


@rules.predicate
def is_allowed_view_vote_count(item_class):
    """Admins are allowed to view vote count at any time, all others only after voting phase."""

    @rules.predicate
    def _view_vote_count(user, module):
        if module:
            return module.has_feature("vote", item_class) & (
                rules_predicates.is_superuser(user)
                | (
                    (
                        is_public_context(user, module)
                        | is_context_member(user, module)
                        | is_context_group_member(user, module)
                        | is_context_moderator(user, module)
                        | is_context_initiator(user, module)
                    )
                    & is_live_context(user, module)
                    & module.module_has_finished
                )
            )
        return False

    return _view_vote_count

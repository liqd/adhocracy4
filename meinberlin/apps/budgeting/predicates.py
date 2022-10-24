import rules
from rules import predicates as rules_predicates

from adhocracy4.modules.predicates import is_context_member
from adhocracy4.modules.predicates import is_live_context
from adhocracy4.modules.predicates import module_is_between_phases
from adhocracy4.phases.predicates import has_feature_active
from adhocracy4.phases.predicates import phase_allows_delete_vote
from adhocracy4.phases.predicates import phase_allows_vote


@rules.predicate
def is_allowed_vote_proposal(user, proposal):
    return rules_predicates.is_superuser(user) | \
        ((not proposal.is_archived)
         & phase_allows_vote(user, proposal)
         & is_live_context(user, proposal))


@rules.predicate
def is_allowed_delete_vote(user, vote):
    return rules_predicates.is_superuser(user) | \
        ((not vote.content_object.is_archived)
         & phase_allows_delete_vote(user, vote)
         & is_live_context(user, vote.content_object))


@rules.predicate
def phase_allows_support(user, item):
    if item:
        return has_feature_active(item.module, item.__class__, 'support')
    return False


@rules.predicate
def is_allowed_support_item(user, item):
    if item:
        return rules_predicates.is_superuser(user) | \
            (is_context_member(user, item) &
             is_live_context(user, item) &
             phase_allows_support(user, item))
    return False


@rules.predicate
def is_allowed_view_support(item_class):
    @rules.predicate
    def _view_support(user, module):
        if module:
            return has_feature_active(module, item_class, 'support')\
                | module_is_between_phases('meinberlin_budgeting:support',
                                           'meinberlin_budgeting:voting',
                                           module)
        return False

    return _view_support

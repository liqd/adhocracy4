import rules
from rules import predicates as rules_predicates

from adhocracy4.modules.predicates import is_live_context
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

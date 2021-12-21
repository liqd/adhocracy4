import rules

from adhocracy4.phases.predicates import phase_allows_vote


@rules.predicate
def is_allowed_vote_proposal(user, proposal):
    return (not proposal.is_archived) and phase_allows_vote(user, proposal)

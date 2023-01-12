import rules


def has_feature_active(module, model, feature):
    if module:
        if not module.active_phase:
            return False
        else:
            return module.active_phase.has_feature(feature, model)
    return False


@rules.predicate
def phase_allows_change(user, item):
    if item:
        return has_feature_active(item.module, item.__class__, "crud")
    return False


def phase_allows_add(item_class):
    @rules.predicate
    def _add_predicate(user, module):
        if module:
            return has_feature_active(module, item_class, "crud")
        return False

    return _add_predicate


@rules.predicate
def phase_allows_comment(user, item):
    if item:
        return has_feature_active(item.module, item.__class__, "comment")
    return False


@rules.predicate
def phase_allows_rate(user, item):
    if item:
        return has_feature_active(item.module, item.__class__, "rate")
    return False


@rules.predicate
def phase_allows_vote(user, item):
    """Given an item, return if its module has voting phase active.

    Used in meinberlin_budgeting.vote_proposal rule to decide
    if a given proposal can be voted on.
    """
    if item:
        return has_feature_active(item.module, item.__class__, "vote")
    return False


@rules.predicate
def phase_allows_delete_vote(user, vote):
    """Return if module of a votes content_object has voting phase active.

    Used in meinberlin_budgeting.delete_vote rule to decide if
    deleting a token vote is allowed.
    """
    if vote:
        return has_feature_active(
            vote.content_object.module, vote.content_object.__class__, "vote"
        )
    return False


def phase_allows_add_vote(item_class):
    """Return if module has voting phase active.

    Used in meinberlin_budgeting.add_vote rule to decide if token
    voting is allowed.
    """

    @rules.predicate
    def _vote_predicate(user, module):
        if module:
            return has_feature_active(module, item_class, "vote")
        return False

    return _vote_predicate

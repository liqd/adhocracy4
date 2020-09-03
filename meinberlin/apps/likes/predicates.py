import rules

from adhocracy4.phases.predicates import has_feature_active


@rules.predicate
def phase_allows_like(user, item):
    if item:
        return has_feature_active(item.module, item.__class__, 'like')
    return False


def phase_allows_like_model(item_class):
    @rules.predicate
    def _add_predicate(user, module):
        if module:
            return has_feature_active(module, item_class, 'like')
        return False
    return _add_predicate

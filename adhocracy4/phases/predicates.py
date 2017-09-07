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
        return has_feature_active(item.module, item.__class__, 'crud')
    return False


def phase_allows_add(item_class):
    @rules.predicate
    def _add_predicate(user, module):
        if module:
            return has_feature_active(module, item_class, 'crud')
        return False
    return _add_predicate


@rules.predicate
def phase_allows_comment(user, item):
    if item:
        return has_feature_active(item.module, item.__class__, 'comment')
    return False


@rules.predicate
def phase_allows_rate(user, item):
    if item:
        return has_feature_active(item.module, item.__class__, 'rate')
    return False

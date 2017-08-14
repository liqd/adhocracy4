import rules


def has_feature_active(module, model, feature):
    module = getattr(module, 'module', module)
    if not module.active_phase:
        return False
    else:
        return module.active_phase.has_feature(feature, model)


@rules.predicate
def phase_allows_change(user, item):
    return has_feature_active(item.module, item.__class__, 'crud')


def phase_allows_add(item_class):
    @rules.predicate
    def _add_predicate(user, module):
        return has_feature_active(module, item_class, 'crud')
    return _add_predicate


@rules.predicate
def phase_allows_comment(user, item):
    return has_feature_active(item.module, item.__class__, 'comment')


@rules.predicate
def phase_allows_rate(user, item):
    return has_feature_active(item.module, item.__class__, 'rate')

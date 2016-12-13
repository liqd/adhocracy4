import rules


def has_feature_active(project, model, feature):
    if not project.active_phase:
        return False
    else:
        return project.active_phase.has_feature(feature, model)


@rules.predicate
def phase_allows_modify(user, item):
    return has_feature_active(item.project, item.__class__, 'crud')


def phase_allows_create(item_class):
    @rules.predicate
    def _create_predicate(user, module):
        return has_feature_active(module.project, item_class, 'crud')
    return _create_predicate


@rules.predicate
def phase_allows_comment(user, item):
    return has_feature_active(item.project, item.__class__, 'comment')


@rules.predicate
def phase_allows_rate(user, item):
    return has_feature_active(item.project, item.__class__, 'rate')

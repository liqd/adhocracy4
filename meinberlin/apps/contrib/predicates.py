import rules


@rules.predicate
def has_started(user, project):
    return project.has_started


@rules.predicate
def has_context_started(user, item):
    return has_started(user, item.project)

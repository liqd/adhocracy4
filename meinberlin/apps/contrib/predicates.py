import rules


@rules.predicate
def has_started(user, project):
    return project.active_phase or len(project.past_phases) > 0


@rules.predicate
def has_context_started(user, item):
    return has_started(user, item.project)

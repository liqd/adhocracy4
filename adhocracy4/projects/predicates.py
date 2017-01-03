import rules


@rules.predicate
def is_member(user, project):
    return project.has_member(user)


@rules.predicate
def is_public(user, project):
    return project.is_public


@rules.predicate
def is_live(user, project):
    return not project.is_draft


@rules.predicate
def is_moderator(user, project):
    return user in project.moderators.all()

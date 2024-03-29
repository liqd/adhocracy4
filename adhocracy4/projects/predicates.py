import warnings

import rules


@rules.predicate
def is_prj_group_member(user, subject):
    if subject:
        if hasattr(subject, "project"):
            warnings.warn(
                "using is_prj_group_member with an item is deprecated; "
                "use is_context_group_member from module predicates instead.",
                DeprecationWarning,
            )
            project = subject.project
        else:
            project = subject
        return project.is_group_member(user)
    return False


@rules.predicate
def is_member(user, project):
    warnings.warn("is_member is deprecated; use is_project_member.", DeprecationWarning)
    return is_project_member(user, project)


@rules.predicate
def is_project_member(user, project):
    if project:
        return project.has_member(user)
    return False


@rules.predicate
def is_public(user, project):
    if project:
        return project.is_public
    return False


@rules.predicate
def is_semipublic(user, project):
    if project:
        return project.is_semipublic
    return False


@rules.predicate
def is_live(user, project):
    if project:
        return not project.is_draft
    return False


@rules.predicate
def is_moderator(user, project):
    if project:
        return user in project.moderators.all()
    return False


@rules.predicate
def has_started(user, project):
    if project:
        return project.has_started
    return False


@rules.predicate
def has_context_started(user, item):
    if item:
        return has_started(user, item.project)
    return False

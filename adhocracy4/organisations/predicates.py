import rules


@rules.predicate
def is_initiator(user, subject):
    if subject:
        if hasattr(subject, 'has_initiator'):
            organisation = subject
        else:
            organisation = subject.organisation
        return organisation.has_initiator(user)
    return False


@rules.predicate
def is_org_group_member(user, organisation):
    if organisation:
        if hasattr(organisation, 'groups'):
            org_groups = organisation.groups.all()
            user_groups = user.groups.all()
            group = org_groups & user_groups
            return group.count() > 0
    return False

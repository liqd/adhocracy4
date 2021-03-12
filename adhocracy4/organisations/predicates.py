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
def is_org_member(user, subject):
    if subject:
        if hasattr(subject, 'has_org_member'):
            organisation = subject
            return organisation.has_org_member(user)
        elif (hasattr(subject, 'organisation') and
              hasattr(subject.organisation, 'has_org_member')):
            organisation = subject.organisation
            return organisation.has_org_member(user)
    return False


@rules.predicate
def is_org_group_member(user, subject):
    if subject:
        if hasattr(subject, 'has_initiator') and hasattr(subject, 'groups'):
            organisation = subject
        elif (hasattr(subject, 'organisation') and
              hasattr(subject.organisation, 'groups')):
            organisation = subject.organisation
        org_groups = organisation.groups.all()
        user_groups = user.groups.all()
        group = org_groups & user_groups
        return group.count() > 0
    return False

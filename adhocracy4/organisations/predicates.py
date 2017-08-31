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

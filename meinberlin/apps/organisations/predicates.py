import rules


@rules.predicate
def is_initiator(user, subject):
    if hasattr(subject, 'initiators'):
        organisation = subject
    else:
        organisation = subject.organisation
    return user in organisation.initiators.all()

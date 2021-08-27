import rules


@rules.predicate
def is_plan_group_member(user, plan):
    if plan:
        return plan.is_group_member(user)
    return False


@rules.predicate
def is_live(user, plan):
    if plan:
        return not plan.is_draft
    return False

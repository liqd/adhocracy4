import rules


@rules.predicate
def is_plan_group_member(user, plan):
    if plan:
        return plan.is_group_member(user)
    return False

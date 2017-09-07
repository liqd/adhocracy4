import rules

from adhocracy4.modules import predicates as module_predicates


@rules.predicate
def content_object_allows_rating(user, rating):
    if rating:
        content_object = rating.content_object
        content_type = rating.content_type
        perm_name = '{app_label}.rate_{model}'.format(
            app_label=content_type.app_label,
            model=content_type.model
        )
        return user.has_perm(perm_name, content_object)
    return False


rules.add_perm(
    'a4ratings.change_rating',
    module_predicates.is_project_admin |
    (
        module_predicates.is_context_member &
        content_object_allows_rating &
        module_predicates.is_owner
    )
)


rules.add_perm(
    'a4ratings.delete_rating',
    module_predicates.is_project_admin |
    (
        content_object_allows_rating &
        module_predicates.is_context_member &
        module_predicates.is_owner
    )
)

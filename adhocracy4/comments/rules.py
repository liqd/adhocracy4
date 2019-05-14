import rules

from adhocracy4.modules import predicates as module_predicates


@rules.predicate
def content_object_allows_comment(user, comment):
    if comment:
        content_object = comment.content_object
        content_type = comment.content_type
        perm_name = '{app_label}.comment_{model}'.format(
            app_label=content_type.app_label,
            model=content_type.model
        )
        return user.has_perm(perm_name, content_object)
    return False


rules.add_perm(
    'a4comments.view_comment',
    module_predicates.is_project_admin |
    module_predicates.is_public_context |
    module_predicates.is_context_member
)


rules.add_perm(
    'a4comments.rate_comment',
    module_predicates.is_project_admin |
    (
        module_predicates.is_context_member &
        content_object_allows_comment
    )
)


rules.add_perm(
    'a4comments.comment_comment',
    module_predicates.is_project_admin |
    (
        module_predicates.is_context_member &
        content_object_allows_comment
    )
)


rules.add_perm(
    'a4comments.change_comment',
    module_predicates.is_project_admin |
    (
        module_predicates.is_context_member &
        content_object_allows_comment &
        module_predicates.is_owner
    )
)


rules.add_perm(
    'a4comments.delete_comment',
    module_predicates.is_project_admin |
    (
        content_object_allows_comment &
        module_predicates.is_context_member &
        module_predicates.is_owner
    )
)

rules.add_perm(
    'a4comments.moderate_comment',
    module_predicates.is_project_admin
)

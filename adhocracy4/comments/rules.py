import rules

from adhocracy4.modules import predicates as module_predicates
from adhocracy4.phases import predicates as phase_predicates


@rules.predicate
def content_object_allows_comment(user, comment):
    if comment:
        content_object = comment.content_object
        return phase_predicates.has_feature_active(
            content_object.module, content_object.__class__, 'comment'
        )
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

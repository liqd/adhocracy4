import rules

from adhocracy4.modules import predicates as module_predicates
from adhocracy4.phases import predicates as phase_predicates


@rules.predicate
def content_object_allows_rating(user, rating):
    content_object = rating.content_object
    return phase_predicates.has_feature_active(
        content_object.module, content_object.__class__, 'rate'
    )


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

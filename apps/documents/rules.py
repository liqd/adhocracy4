import rules

from adhocracy4.modules import predicates as module_predicates


rules.add_perm(
    'meinberlin_documents.view_document',
    module_predicates.is_allowed_view_item
)


rules.add_perm(
    'meinberlin_documents.add_document',
    module_predicates.is_project_admin
)


rules.add_perm(
    'meinberlin_documents.change_document',
    module_predicates.is_project_admin
)


rules.add_perm(
    'meinberlin_documents.comment_paragraph',
    module_predicates.is_allowed_comment_item
)

rules.add_perm(
    'meinberlin_documents.comment_document',
    module_predicates.is_allowed_comment_item
)

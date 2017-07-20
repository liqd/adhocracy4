import rules

from adhocracy4.modules import predicates as module_predicates
from meinberlin.apps.contrib import predicates as contrib_predicates

rules.add_perm(
    'meinberlin_documents.view_chapter',
    (module_predicates.is_project_admin |
     (module_predicates.is_allowed_view_item &
      contrib_predicates.has_context_started))
)

rules.add_perm(
    'meinberlin_documents.view_paragraph',
    (module_predicates.is_project_admin |
     (module_predicates.is_allowed_view_item &
      contrib_predicates.has_context_started))
)

rules.add_perm(
    'meinberlin_documents.add_chapter',
    module_predicates.is_project_admin
)

rules.add_perm(
    'meinberlin_documents.change_chapter',
    module_predicates.is_project_admin
)

rules.add_perm(
    'meinberlin_documents.comment_paragraph',
    module_predicates.is_allowed_comment_item
)

rules.add_perm(
    'meinberlin_documents.comment_chapter',
    module_predicates.is_allowed_comment_item
)

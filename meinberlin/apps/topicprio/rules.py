import rules

from adhocracy4.modules import predicates as module_predicates
from meinberlin.apps.contrib import predicates as contrib_predicates

rules.add_perm(
    'meinberlin_topicprio.add_topic',
    module_predicates.is_project_admin
)

rules.add_perm(
    'meinberlin_topicprio.change_topic',
    module_predicates.is_project_admin
)

rules.add_perm(
    'meinberlin_topicprio.view_topic',
    (module_predicates.is_project_admin |
     (module_predicates.is_allowed_view_item &
      contrib_predicates.has_context_started))
)

rules.add_perm(
    'meinberlin_topicprio.rate_topic',
    module_predicates.is_allowed_rate_item
)

rules.add_perm(
    'meinberlin_topicprio.comment_topic',
    module_predicates.is_allowed_comment_item
)

rules.add_perm(
    'meinberlin_topicprio.moderate_topic',
    module_predicates.is_context_moderator |
    module_predicates.is_context_initiator
)

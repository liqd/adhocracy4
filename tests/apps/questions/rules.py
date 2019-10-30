import rules

from adhocracy4.modules.predicates import is_allowed_comment_item
from adhocracy4.modules.predicates import is_allowed_rate_item

rules.add_perm('a4test_questions.comment_question', is_allowed_comment_item)


rules.add_perm('a4test_questions.rate_question', is_allowed_rate_item)

rules.add_perm(
    'a4test_questions.always_allow',
    rules.predicates.is_authenticated
)

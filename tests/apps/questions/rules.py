import rules

from rules.predicates import is_authenticated

rules.add_perm('a4test_questions.comment_question', is_authenticated)

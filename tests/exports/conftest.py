from pytest_factoryboy import register

from adhocracy4.test.factories import categories as category_factories
from adhocracy4.test.factories import labels as label_factories
from tests.apps.ideas import factories as idea_factories
from tests.apps.moderatorfeedback import factories as moderatorfeedback_factories
from tests.apps.questions import factories as question_factories
from tests.comments import factories as comment_factories
from tests.ratings import factories as rating_factories

register(idea_factories.IdeaFactory)
register(moderatorfeedback_factories.ModeratorFeedbackFactory)
register(question_factories.QuestionFactory)
register(category_factories.CategoryFactory)
register(category_factories.CategoryAliasFactory)
register(comment_factories.CommentFactory)
register(label_factories.LabelFactory)
register(label_factories.LabelAliasFactory)
register(rating_factories.RatingFactory)

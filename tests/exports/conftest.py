from pytest_factoryboy import register

from tests.apps.ideas import factories as idea_factories
from tests.categories import factories as category_factories
from tests.comments import factories as comment_factories
from tests.ratings import factories as rating_factories

register(category_factories.CategoryFactory)
register(idea_factories.IdeaFactory)
register(rating_factories.RatingFactory)
register(comment_factories.CommentFactory)

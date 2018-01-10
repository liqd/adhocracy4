from pytest_factoryboy import register

from tests.apps.ideas import factories as idea_factories
from tests.ratings import factories as rating_factories
from tests.comments import factories as comment_factories

register(idea_factories.IdeaFactory)
register(rating_factories.RatingFactory)
register(comment_factories.CommentFactory)

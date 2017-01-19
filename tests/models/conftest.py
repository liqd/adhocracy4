from pytest_factoryboy import register

from tests.comments import factories as comments_factories
from tests.ratings import factories as ratings_factories

register(comments_factories.CommentFactory)
register(ratings_factories.RatingFactory)

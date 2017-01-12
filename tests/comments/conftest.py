from pytest_factoryboy import register

from . import factories as comment_factories
from tests.ratings import factories as rating_factories

register(rating_factories.RatingFactory)
register(comment_factories.CommentFactory)

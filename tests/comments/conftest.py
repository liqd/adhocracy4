from pytest_factoryboy import register

from tests.ratings import factories as rating_factories

from . import factories as comment_factories

register(rating_factories.RatingFactory)
register(comment_factories.CommentFactory)

from pytest_factoryboy import register

from tests.ratings import factories as ratings_factories

register(ratings_factories.RatingFactory)

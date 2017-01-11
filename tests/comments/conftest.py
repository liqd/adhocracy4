from pytest_factoryboy import register

import factories as comment_factories
from tests.apps.fakeprojects import factories as fprojects_factories
from tests.ratings import factories as rating_factories

register(fprojects_factories.FakeProjectContentFactory)
register(rating_factories.RatingFactory)
register(comment_factories.CommentFactory)

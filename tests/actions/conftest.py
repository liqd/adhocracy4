from pytest_factoryboy import register

from tests.actions import factories
from tests.comments import factories as comments_factories

register(comments_factories.CommentFactory)
register(factories.ActionFactory)

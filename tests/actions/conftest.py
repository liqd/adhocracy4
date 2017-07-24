from pytest_factoryboy import register

from tests.comments import factories as comments_factories

from tests.actions import factories

register(comments_factories.CommentFactory)
register(factories.ActionFactory)

from pytest_factoryboy import register

from tests.comments.factories import CommentFactory
from tests.reports import factories

register(CommentFactory)
register(factories.ReportFactory)
